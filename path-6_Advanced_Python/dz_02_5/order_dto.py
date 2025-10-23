from datetime import datetime

class OrderDTO:
    def __init__(self, order_id: int, customer_name: str, product_name: str, company_name: str, order_date: datetime):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.company_name = company_name
        self.order_date = order_date

    def __repr__(self):
        return f"OrderDTO(id={self.order_id}, customer='{self.customer_name}', product='{self.product_name}', company='{self.company_name}', date={self.order_date})"