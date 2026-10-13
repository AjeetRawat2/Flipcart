# Flipkart style storefront showcase

A responsive Django storefront inspired by Flipkart, built as a portfolio showcase. It includes a browsable product catalog, search and category filters, product details, a session cart, saved items, Django demo accounts, order history, delivery address collection, and cash on delivery.

## Payment behavior

The online payment path is intentionally simulated. It never connects to a payment provider, accepts card or UPI details, or charges money. It creates a demo order and marks it confirmed only when the visitor confirms the on-page simulation.

## Run locally

1. Install Python 3.11+.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Apply database migrations: `python manage.py migrate`.
4. Start the site: `python manage.py runserver`.

Open `http://127.0.0.1:8000`. Use sample details to create a showcase account. Local development uses SQLite at `db.sqlite3`.

## Deploy on Vercel

Vercel detects the Django `manage.py`, WSGI application, and collected static files. Set `DJANGO_SECRET_KEY` in the Vercel project environment for preview and production. Set `DJANGO_DEBUG=false`. `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` can be used for custom domains.

The Vercel showcase database uses temporary SQLite storage under `/tmp`; it is not durable across serverless instances or redeploys. Accounts, carts, and orders are demonstrations and should not be used for real customers. Use a managed database and production authentication/payment providers before operating a real store.
