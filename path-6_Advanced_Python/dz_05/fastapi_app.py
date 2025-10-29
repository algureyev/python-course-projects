from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from config import DB_CONFIG
from connection import Connection
from tables.suppliers import Suppliers
from pydantic import BaseModel

# Модели Pydantic
class SupplierResponse(BaseModel):
    id: int
    seller_id: int
    company_name: str
    contact_person: str
    phone: str

    class Config:
        from_attributes = True

class SupplierUpdate(BaseModel):
    company_name: str | None = None
    contact_person: str | None = None
    phone: str | None = None

# Создаем FastAPI приложение
app = FastAPI(
    title="Suppliers API",
    description="API для работы с продавцами",
    version="1.0.0"
)

# Создаем подключение к БД
connection = Connection(**DB_CONFIG)
engine = connection.engine
SessionLocal = sessionmaker(bind=engine)

@app.get("/")
def root():
    """Проверка работы API"""
    return {"message": "Suppliers API is running"}

@app.get("/sallers")
def get_all_suppliers():
    """Получение всех продавцов"""
    db = SessionLocal()
    try:
        suppliers = db.query(Suppliers).all()
        return suppliers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/sallers/{supplier_id}")
def get_supplier_by_id(supplier_id: int):
    """Получение продавца по ID"""
    db = SessionLocal()
    try:
        supplier = db.query(Suppliers).filter(Suppliers.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.put("/sallers/{supplier_id}/update")
def update_supplier(supplier_id: int, supplier_data: SupplierUpdate):
    """Обновление данных продавца"""
    db = SessionLocal()
    try:
        supplier = db.query(Suppliers).filter(Suppliers.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Обновляем только переданные поля
        update_data = supplier_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(supplier, field, value)
        
        db.commit()
        db.refresh(supplier)
        return supplier
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)