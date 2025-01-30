from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt

def role_required(role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()

            user_role = claims.get('role', None)
            user_id = claims.get('sub', None)

            # Log user role and access attempt
            current_app.logger.info(f"User ID {user_id} attempting to access a route with role: {user_role}")

            if user_role != role:
                # Log failed access attempt
                current_app.logger.warning(f"Access denied for User ID {user_id}. {role.capitalize()} access required.")
                return jsonify(message=f"{role.capitalize()} access required"), 403

            # Log successful access
            current_app.logger.info(f"User ID {user_id} granted access to {role.capitalize()} route.")
            return f(user_id=user_id, *args, **kwargs)
        return decorated_function
    return decorator