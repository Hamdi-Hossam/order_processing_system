from flask import jsonify, request
import stripe
from app.models.order import Order
from app.extensions import database
from app.services.email_service import send_order_confirmation
import os
from flask import current_app

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def pay_order(user_id, order_id,card_number,card_cvv,card_exp_month,card_exp_year):
    try:
        # Fetch the order from the database
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            current_app.logger.error(f"Order with ID {order_id} not found for user {user_id}")
            return jsonify({"error": "Order not found"}), 404
        
        # Check if the order is already paid
        if order.status == 'Completed' and order.payment_status == "Paid":
            current_app.logger.warning(f"Order {order_id} for user {user_id} is already paid and completed")
            return jsonify({"error": "Order already paid"}), 400

        # Validate the card info
        if len(card_cvv) == 3 and len(card_number) == 16 and card_exp_month in range(1, 13) and card_exp_year >= 2025:
            payment_status = "succeeded"
            current_app.logger.info(f"Payment simulated successfully for order {order_id} by user {user_id}")
        else:
            payment_status = "failed"
            current_app.logger.warning(f"Payment failed for order {order_id} by user {user_id}")
            return jsonify({"error": "Invalid card details or payment failed"}), 400
        # Create a Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            description=f"Payment for Order #{order.id}",
            metadata={"order_id": order.id},
            automatic_payment_methods={"enabled": True}
        )
        # Updating order status
        if payment_status == "succeeded":
            intent.status == "succeeded"
            order.payment_status = "Paid"
            order.status = "Completed"
            database.session.commit()

            # Sending mail
            send_order_confirmation(order_id)

            current_app.logger.info(f"Payment successful for order {order_id} by user {user_id}")
            return jsonify({"message": "Payment simulated successfully", "order_status": order.status})

        else:
            return jsonify({"error": "Payment simulation failed"}), 400

    except stripe.error.StripeError as e:
        current_app.logger.error(f"Stripe error for order {order_id} for user {user_id}: {str(e)}")
        return jsonify({"error": "Payment processing error"}), 500
    except Exception as e:
        current_app.logger.exception(f"Error processing payment for order {order_id} for user {user_id}")
        return jsonify({"error": str(e)}), 500
