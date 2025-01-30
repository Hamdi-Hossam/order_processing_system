from app.extensions import database

class OrderProduct(database.Model):
    __tablename__ = 'order_product'

    order_id = database.Column(database.Integer, database.ForeignKey('orders.id'), primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('products.id'), primary_key=True)
    quantity = database.Column(database.Integer, nullable=False)
    product = database.relationship('Product', back_populates='order_products', lazy=True)
    order = database.relationship('Order', back_populates='order_products', lazy=True)
    
    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
