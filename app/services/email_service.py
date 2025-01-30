from flask_mail import Message
from app import mail
from app.models.user import User
from app.models.order import Order
from flask import current_app

def send_order_confirmation(order_id):
    try:
        # Retrieve the order and user details
        order = Order.query.get(order_id)
        if not order:
            current_app.logger.error(f"Order not found with ID: {order_id}")
            return {"error": "Order not found"}, 404
        
        user = User.query.get(order.user_id)
        if not user:
            current_app.logger.error(f"User not found for order ID: {order_id}")
            return {"error": "User not found"}, 404

        # Email content
        subject = "Order Confirmation"
        recipient = user.email
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f9; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h2 style="color: #2d3e50;">Order Confirmation</h2>
                    <p style="font-size: 16px;">Dear <strong>{user.username}</strong>,</p>
                    <p style="font-size: 16px;">Thank you for your order! Your order has been successfully placed.</p>
                    <p style="font-size: 16px;"><strong>Order ID:</strong> {order.id}</p>
                    <p style="font-size: 16px;"><strong>Total Amount:</strong> ${order.total_amount}</p>
                    <p style="font-size: 16px;"><strong>Status:</strong> {order.status}</p>
                    
                    <h3 style="color: #2d3e50;">Products:</h3>
                    <ul style="list-style-type: none; padding: 0; font-size: 16px;">
        """
        
        for order_product in order.order_products:
            product = order_product.product
            body += f"""
                    <li style="padding: 8px 0; border-bottom: 1px solid #eee;">
                        <strong>{product.name}</strong> x {order_product.quantity} 
                        at <strong>${product.price}</strong>
                    </li>
            """
        
        body += f"""
                    </ul>
                    <p style="font-size: 16px;">We appreciate your business and hope to serve you again soon!</p>
                    <p style="font-size: 14px; color: #999;">This is an automated message. Please do not reply.</p>
                </div>
            </body>
        </html>
        """
        
        # Sending the email
        msg = Message(subject=subject, recipients=[recipient], html=body)
        mail.send(msg)
        current_app.logger.info(f"Order confirmation sent for order ID: {order_id} to {recipient}")

    except Exception as e:
        current_app.logger.exception(f"Error sending order confirmation for order ID: {order_id}")
        return {"error": f"An error occurred: {str(e)}"}, 500
