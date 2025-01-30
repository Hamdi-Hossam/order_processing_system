from flask import Blueprint, request, jsonify, current_app
from app.services.product_service import add_product, get_products
from app.middleware.role import role_required

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/add', methods=['POST'])
@role_required('admin')
def add_new_product():
    data = request.get_json()
    
    try:
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        
        if not name or not price or price <= 0:
            current_app.logger.warning(f"Failed to add product, invalid data: {data}")
            return jsonify({"error": "Invalid product data."}), 400
        
        product = add_product(name, description, price, stock)

        current_app.logger.info(f"Product added successfully: {product.id}, {product.name}")
        
        return jsonify({
            "message": "Product added successfully.",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock
            }
        }), 201

    except ValueError as e:
        current_app.logger.error(f"Value error when adding product: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception(f"Unexpected error while adding product: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@product_routes.route('/get', methods=['GET'])
@role_required('admin')
def get_all_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', None, type=str)
        products = get_products(page=page, per_page=per_page, search=search)
        
        if not products:
            current_app.logger.error("Failed to retrieve products from the database.")
            return jsonify({"error": "Failed to retrieve products, please try again later."}), 500
        
        product_list = [{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        } for product in products.items]
        
        current_app.logger.info(f"Successfully retrieved {len(product_list)} products.")
        
        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": products.total,
            "products": product_list
        })
    
    except Exception as e:
        current_app.logger.exception(f"Error occurred while retrieving products: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
