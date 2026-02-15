from flask import Blueprint, jsonify, request

from app.services.order_service import OrderService


orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/orders")
def get_orders():
    orders = OrderService.fetch_all_orders()
    return jsonify(orders), 200


@orders_bp.get("/orders/<int:order_id>")
def get_order_by_id(order_id: int):
    order = OrderService.fetch_order_by_id(order_id)
    if order is None:
        return jsonify({"message": f"Order with id {order_id} not found"}), 404
    return jsonify(order), 200


@orders_bp.post("/orders")
def create_order():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"message": "Request body must be valid JSON"}), 400

    try:
        order = OrderService.create_order(payload)
    except ValueError as exc:
        return jsonify({"message": "Validation failed", "errors": exc.args[0]}), 400
    except RuntimeError as exc:
        return jsonify({"message": str(exc)}), 500

    return jsonify(order), 201


@orders_bp.get("/orderitems")
def get_order_items():
    order_items = OrderService.fetch_order_items()
    return jsonify(order_items), 200


@orders_bp.get("/orderitems/<int:order_id>")
def get_order_items_by_id(order_id: int):
    order = OrderService.fetch_order_items_by_id(order_id)
    if order is None:
        return jsonify({"message": f"Order with id {order_id} not found"}), 404
    return jsonify(order), 200

