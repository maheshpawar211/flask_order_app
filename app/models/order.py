from datetime import datetime
from sqlalchemy import CheckConstraint
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"
    __table_args__ = {"schema": "sa123"}

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="PENDING")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy=True,
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"
    __table_args__ = {"schema": "sa123"}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("sa123.orders.id"), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", back_populates="items")
    __table_args__ = (
            CheckConstraint("price >= 0", name="ck_order_items_price_non_negative"),
            {"schema": "sa123"},
    )