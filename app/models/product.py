from app.extensions import database

class Product(database.Model):
    __tablename__ = 'products'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    description = database.Column(database.String(255))
    price = database.Column(database.Float, nullable=False)
    stock = database.Column(database.Integer, default=0)
    order_products = database.relationship('OrderProduct', back_populates='product', lazy=True, overlaps="orders")


    def __init__(self, name, description, price, stock):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
