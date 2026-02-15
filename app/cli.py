import click

from .extensions import db
from .models import Order, OrderItem


def register_cli_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("seed-demo")
    def seed_demo():
        """Seed sample order data for quick testing."""
        if Order.query.first():
            click.echo("Orders already exist. Seed skipped.")
            return

        order_1 = Order(customer_name="Alice Johnson", status="CONFIRMED")
        order_1.items = [
            OrderItem(product_name="Keyboard", quantity=1, price=79.99),
            OrderItem(product_name="Mouse", quantity=2, price=25.5),
        ]

        order_2 = Order(customer_name="Bob Smith", status="PENDING")
        order_2.items = [
            OrderItem(product_name="Monitor", quantity=1, price=220.0),
        ]

        db.session.add_all([order_1, order_2])
        db.session.commit()
        click.echo("Demo orders inserted.")
