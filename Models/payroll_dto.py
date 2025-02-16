from datetime import datetime

class PayRollDto:
    def __init__(self, email: str, read_date: datetime, full_name: str, position: str, 
                 health_discount_amount: float, social_discount_amount: float, 
                 taxes_discount_amount: float, other_discount: float, 
                 gross_salary: float, gross_payment: float,net_payment: float, period: str):
        self.email = email
        self.read_date = read_date
        self.full_name = full_name
        self.position = position
        self.health_discount_amount = health_discount_amount
        self.social_discount_amount = social_discount_amount
        self.taxes_discount_amount = taxes_discount_amount
        self.other_discount = other_discount
        self.gross_salary = gross_salary
        self.gross_payment = gross_payment
        self.net_payment = net_payment
        self.period = period
        self.total = social_discount_amount+health_discount_amount+taxes_discount_amount+other_discount

    def to_dict(self):
        return {
            'email': self.email,
            'read_date': self.read_date
        }