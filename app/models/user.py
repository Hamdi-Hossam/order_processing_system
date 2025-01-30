from app.extensions import database
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from app.models.order import Order

class User(database.Model):
    __tablename__ = 'users'
    
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password_hash = database.Column(database.String(128), nullable=False)
    role = database.Column(database.String(50), nullable=False)
    orders = relationship('Order', backref='user', lazy=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
