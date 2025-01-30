from flask import Flask
from app.extensions import database, mail, jwt, migrate
from app.routes.user_routes import user_routes
from app.routes.product_routes import product_routes
from app.routes.order_routes import order_routes
from app.routes.payment_routes import payment_routes
from app.config import Config
from app.handlers import init_error_handlers




def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    Config.init_app(app)


    # Initialize extensions
    database.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, database)
    init_error_handlers(app)


    # Register blueprints
    app.register_blueprint(user_routes, url_prefix="/api/users")
    app.register_blueprint(product_routes, url_prefix="/api/products")
    app.register_blueprint(order_routes, url_prefix="/api/orders")
    app.register_blueprint(payment_routes, url_prefix="/api/payments")

    return app
