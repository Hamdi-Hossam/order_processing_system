from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import database
from flask import current_app

def register_user(username, email, password, role=None):
    try:
        # If role provided it will be considered else it will be buyer
        role = role if role else "buyer"

        if role not in ["admin", "buyer"]:
            current_app.logger.error(f"Invalid role: {role}")
            return {"error": "Invalid role"}, 400
        
        if User.query.filter_by(email=email).first():
            current_app.logger.error(f"Email already registered: {email}")
            return {"error": "Email already registered"}, 400
        
        if User.query.filter_by(username=username).first():
            current_app.logger.error(f"Username already registered: {username}")
            return {"error": "Username already registered"}, 400

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        database.session.add(new_user)
        database.session.commit()

        current_app.logger.info(f"User registered successfully: {username} ({email})")
        return {"message": "User registered successfully"}, 201

    except Exception as e:
        current_app.logger.exception("Error registering user")
        return {"error": f"An error occurred: {str(e)}"}, 500

def login_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            current_app.logger.info(f"User logged in successfully: {email}")
            return {"access_token": access_token}, 200

        current_app.logger.warning(f"Invalid login attempt: {email}")
        return {"error": "Invalid credentials"}, 401

    except Exception as e:
        current_app.logger.exception("Error during login")
        return {"error": f"An error occurred: {str(e)}"}, 500
