from flask import Blueprint, jsonify, current_app, request
from app.services.payment_service import pay_order
from app.middleware.role import role_required

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route('/pay/<int:order_id>', methods=['POST'])
@role_required('buyer')
def pay(user_id, order_id):
    data = request.json
    
    card_number = data.get("card_number")
    card_cvv = data.get("card_cvv")
    card_exp_month = data.get("card_exp_month")
    card_exp_year = data.get("card_exp_year")

    if not card_number or not card_cvv or not card_exp_month or not card_exp_year:
        current_app.logger.warning(f"Payment attempt failed. Missing fields: {data}")
        return jsonify({"error": "Card number, CVV, Expiry month and Expiry year are required."}), 400
    

    try:
        response = pay_order(user_id, order_id, card_number, card_cvv, card_exp_month, card_exp_year)
        
        current_app.logger.info(f"Payment attempt for order {order_id} by user {user_id}: {response}")
        
        return response
    except Exception as e:
        current_app.logger.exception(f"Error processing payment for order {order_id} by user {user_id}: {str(e)}")
        return jsonify({"error": "An error occurred while processing your payment. Please try again later."}), 500
