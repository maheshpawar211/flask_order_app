from flask import Blueprint

from .orders import orders_bp


api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(orders_bp)
