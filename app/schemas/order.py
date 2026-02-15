from marshmallow import fields, validate

from app.extensions import ma
from app.models import Order, OrderItem


class OrderItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderItem
        load_instance = True

    id = ma.auto_field()
    product_name = ma.auto_field()
    quantity = ma.auto_field()
    #price = ma.auto_field()
    price = fields.Float(required=True, validate=validate.Range(min=0))


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = ma.auto_field()
    customer_name = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field()
    items = ma.Nested(OrderItemSchema, many=True)


class OrderItemCreateSchema(ma.Schema):
    product_name = fields.String(required=True, validate=validate.Length(min=1))
    quantity = fields.Integer(load_default=1, validate=validate.Range(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))


class OrderCreateSchema(ma.Schema):
    customer_name = fields.String(required=True, validate=validate.Length(min=1))
    status = fields.String(load_default="PENDING")
    items = fields.List(
        fields.Nested(OrderItemCreateSchema),
        required=True,
        validate=validate.Length(min=1),
    )


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_order_input_schema = OrderCreateSchema()
