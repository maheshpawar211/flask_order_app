# Flask Order Microservice (Factory Pattern)

This project is a Flask microservice that fetches orders from `orders` and `order_items` tables using the Flask app factory pattern.

## Project Structure

```
.
|-- app
|   |-- __init__.py
|   |-- api
|   |   |-- __init__.py
|   |   `-- orders.py
|   |-- cli.py
|   |-- extensions.py
|   |-- models
|   |   |-- __init__.py
|   |   `-- order.py
|   |-- schemas
|   |   |-- __init__.py
|   |   `-- order.py
|   `-- services
|       |-- __init__.py
|       `-- order_service.py
|-- config.py
|-- requirements.txt
|-- run.py
`-- wsgi.py
```

## Local Setup

1. Create venv and install deps:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment and run migrations:

```bash
set APP_ENV=development
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/appdb_dev
flask --app run.py db init
flask --app run.py db migrate -m "initial"
flask --app run.py db upgrade
```

3. Optional: seed demo data:

```bash
flask --app run.py seed-demo
```

4. Run service:

```bash
flask --app run.py run
```

## API Endpoints

- `GET /health`
- `GET /api/v1/orders`
- `GET /api/v1/orders/<order_id>`
- `POST /api/v1/orders`
- `GET /api/v1/orderitems`

## Example

```bash
curl http://127.0.0.1:5000/api/v1/orders
```

## Dev / QA / Prod Migration Flow

Use the same migration scripts in all environments:

```bash
flask --app run.py db upgrade
```

Set env vars per environment before upgrade:

- Dev: `APP_ENV=development`, `DATABASE_URL=.../appdb_dev`
- QA: `APP_ENV=qa`, `DATABASE_URL=.../appdb_qa`
- Prod: `APP_ENV=production`, `DATABASE_URL=.../appdb_prod`

## Docker Compose By Environment (App Container Only)

Base + environment override:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
docker compose -f docker-compose.yml -f docker-compose.qa.yml up --build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

Each startup runs:

```bash
flask --app run.py db upgrade
```
