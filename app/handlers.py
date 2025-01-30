from flask import jsonify

def init_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f"404 Error: {str(error)}")
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Error: {str(error)}")
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled Exception: {str(error)}")
        return jsonify({"error": "Internal Error", "message": "An unexpected error occurred."}), 500
