from app.models.product import Product
from app.extensions import database
from flask import current_app

def add_product(name, description, price, stock):
    try:
        # Validate input data
        if not name or not price or price <= 0:
            current_app.logger.error(f"Invalid product data: name={name}, price={price}, stock={stock}")
            raise ValueError("Invalid product data.")
        
        # Create new product
        product = Product(name=name, description=description, price=price, stock=stock)
        
        database.session.add(product)
        database.session.commit()

        current_app.logger.info(f"Product added successfully: {product.name}, Price: {product.price}, Stock: {product.stock}")
        
        return product
    except ValueError as e:
        current_app.logger.warning(f"Error adding product: {str(e)}")
        raise
    except Exception as e:
        current_app.logger.exception(f"Unexpected error when adding product: {str(e)}")
        raise

def get_products(page=1, per_page=10, search=None):
    try:
        query = Product.query
        
        # Apply search
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        
        # Pagination
        products = query.paginate(page=page, per_page=per_page, error_out=False)
        
        current_app.logger.info(f"Retrieved products: page={page}, per_page={per_page}, search={search}")
        
        return products
    except Exception as e:
        current_app.logger.exception(f"Unexpected error when retrieving products: {str(e)}")
        raise
