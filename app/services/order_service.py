from app.models.order import Order
from app.models.product import Product
from app.models.orderxproduct import OrderProduct
from app.extensions import database
from flask import current_app

def validate_stock_and_create_order(user_id, product_quantities):
    try:
        products = []
        total_amount = 0

        for product_id, quantity in product_quantities.items():
            product = Product.query.get(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist.")
            if product.stock < quantity:
                raise ValueError(f"Not enough stock for product {product.name}")
            products.append((product, quantity))
            total_amount += product.price * quantity

        order = Order(user_id=user_id, total_amount=total_amount)
        database.session.add(order)
        database.session.commit()

        for product, quantity in products:
            order_product = OrderProduct(order_id=order.id, product_id=product.id, quantity=quantity)
            database.session.add(order_product)

            product.stock -= quantity

        database.session.commit()
        current_app.logger.info(f"Order created successfully for user {user_id} with total amount ${total_amount}")
        return order

    except ValueError as e:
        current_app.logger.error(f"Validation error in order creation: {str(e)}")
        raise e
    except Exception as e:
        current_app.logger.exception(f"Error during order creation for user {user_id}")
        raise e


def get_user_orders(user_id):
    try:
        orders = Order.query.filter_by(user_id=user_id).all()
        orders_list = []

        for order in orders:
            order_data = {
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "payment_status": order.payment_status,
                "order_products": []
            }
            for product in order.products:
                order_product = OrderProduct.query.filter_by(order_id=order.id, product_id=product.id).first()

                order_data["order_products"].append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "price": product.price,
                    "quantity": order_product.quantity if order_product else 0
                })

            orders_list.append(order_data)

        current_app.logger.info(f"Fetched {len(orders_list)} orders for user {user_id}")
        return orders_list

    except Exception as e:
        current_app.logger.exception(f"Error fetching orders for user {user_id}")
        raise e
