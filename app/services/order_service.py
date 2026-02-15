from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Order, OrderItem
from app.schemas import create_order_input_schema, order_schema, orders_schema


class OrderService:
    @staticmethod
    def fetch_all_orders() -> list[dict]:
        orders = Order.query.order_by(Order.id.desc()).all()
        return orders_schema.dump(orders)

    @staticmethod
    def fetch_order_by_id(order_id: int) -> dict | None:
        order = Order.query.get(order_id)
        if order is None:
            return None
        return order_schema.dump(order)

    @staticmethod
    def create_order(payload: dict) -> dict:
        try:
            data = create_order_input_schema.load(payload)
        except ValidationError as exc:
            raise ValueError(exc.messages) from exc

        order = Order(customer_name=data["customer_name"], status=data["status"])
        order.items = [
            OrderItem(
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"],
            )
            for item in data["items"]
        ]

        try:
            db.session.add(order)
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RuntimeError("Failed to create order") from exc

        return order_schema.dump(order)

    @staticmethod
    def fetch_order_items() -> list[dict]:
        rows = (
            db.session.query(Order, OrderItem)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .order_by(Order.id.desc(), OrderItem.id.asc())
            .all()
        )

        return [
            {
                "order_id": order.id,
                "customer_name": order.customer_name,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "order_item_id": item.id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for order, item in rows
        ]


    @staticmethod
    def fetch_order_items_by_id(order_id: int) -> dict | None:
        rows = (
            db.session.query(Order, OrderItem)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .filter(Order.id == order_id)
        )

        return [
            {
                "order_id": order.id,
                "customer_name": order.customer_name,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "order_item_id": item.id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for order, item in rows
        ]
