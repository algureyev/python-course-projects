from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from connection import Connection

class SessionBuilder:
    def __init__(self, connection: Connection) -> None:
        self.engine = create_engine(connection.engine)
        self.async_engine = create_async_engine(connection.async_engine)

    def build(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def async_build(self):
        Session = sessionmaker(
            bind=self.async_engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        return Session()