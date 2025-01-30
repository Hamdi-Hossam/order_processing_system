from flask import Blueprint, request, jsonify, current_app
from app.services.order_service import validate_stock_and_create_order, get_user_orders
from app.middleware.role import role_required

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/add', methods=['POST'])
@role_required('buyer')
def create_order(user_id):
    data = request.get_json()
    
    if 'product_quantities' not in data:
        current_app.logger.warning("Missing 'product_quantities' in the request body.")
        return jsonify({"error": "Missing 'product_quantities' in request body"}), 400
    
    product_quantities = data['product_quantities']
    
    try:
        order = validate_stock_and_create_order(user_id, product_quantities)
        current_app.logger.info(f"Order created successfully: {order.id} for user {user_id}")
        return jsonify({"message": "Order placed successfully!", "order_id": order.id}), 200
    except ValueError as e:
        current_app.logger.warning(f"Validation error while creating order for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception(f"Unexpected error while creating order for user {user_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@order_routes.route('/get', methods=['GET'])
@role_required('buyer')
def get_orders(user_id):
    try:
        orders = get_user_orders(user_id)
        current_app.logger.info(f"Retrieved {len(orders)} orders for user {user_id}")
        return jsonify({"orders": orders}), 200
    except Exception as e:
        current_app.logger.exception(f"Unexpected error while retrieving orders for user {user_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
