from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


database = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
migrate = Migrate()