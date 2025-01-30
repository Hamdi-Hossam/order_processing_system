from flask import Blueprint, request, current_app, jsonify
from app.services.auth_service import register_user, login_user


user_routes = Blueprint("users", __name__)


@user_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    
    if not username or not email or not password or not role:
        current_app.logger.warning(f"Registration attempt failed. Missing fields: {data}")
        return jsonify({"error": "All fields (username, email, password, role) are required."}), 400
    
    if len(password) < 6:
        current_app.logger.warning(f"Registration attempt failed. Weak password: {data}")
        return jsonify({"error": "Password must be at least 6 characters long."}), 400

    try:
        current_app.logger.info(f"User registration started for email: {email}")
        return register_user(username, email, password, role)
    except ValueError as e:
        current_app.logger.error(f"Registration failed for email: {email}, Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error during registration for email: {email}, Error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@user_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        current_app.logger.warning(f"Login attempt failed. Missing fields: {data}")
        return jsonify({"error": "Email and password are required."}), 400
    
    try:
        current_app.logger.info(f"Login attempt for email: {email}")
        return login_user(email, password)
    except ValueError as e:
        current_app.logger.error(f"Login failed for email: {email}, Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error during login for email: {email}, Error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500