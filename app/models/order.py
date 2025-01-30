from datetime import datetime
from app.extensions import database
from app.models.orderxproduct import OrderProduct

class Order(database.Model):
    __tablename__ = 'orders'
    
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    total_amount = database.Column(database.Float, nullable=False)
    status = database.Column(database.String(50), default="Pending")
    created_at = database.Column(database.DateTime, default=datetime.utcnow)
    payment_status = database.Column(database.String(50), default="Unpaid")
    stripe_payment_intent_id = database.Column(database.String(255))
    order_products = database.relationship('OrderProduct', back_populates='order', lazy=True, overlaps="products")



    
    def __init__(self, user_id, total_amount):
        self.user_id = user_id
        self.total_amount = total_amount
