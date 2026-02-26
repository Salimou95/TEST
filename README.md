# ShopDjango — E-commerce App

A full-stack e-commerce application with a **React** frontend and a **Django REST Framework** backend.

## Architecture

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React 18 + Vite + React Router DOM  |
| Backend  | Django 5 + Django REST Framework    |
| Database | MySQL                               |
| Auth     | Django session authentication       |

## Backend (Django REST API)

### Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API runs on `http://localhost:8000`. All endpoints are under `/api/`.

### API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/csrf/` | Get CSRF token |
| GET | `/api/categories/` | List categories |
| GET | `/api/products/` | List products (filter: `?category=<slug>`) |
| GET | `/api/products/<id>/` | Product detail |
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/user/` | Current user info |
| GET/PUT | `/api/auth/profile/` | User profile |
| GET | `/api/cart/` | Cart contents |
| POST | `/api/cart/add/<product_id>/` | Add item to cart |
| POST | `/api/cart/remove/<product_id>/` | Remove item from cart |
| GET | `/api/orders/` | Order history |
| POST | `/api/orders/checkout/` | Place an order |
| GET | `/api/orders/<id>/` | Order detail |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | dev key | Django secret key |
| `DJANGO_DEBUG` | `0` | Enable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed hosts |
| `DB_NAME` | — | MySQL database name |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | — | MySQL password |
| `DB_HOST` | `localhost` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,...` | React dev server origins |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:5173,...` | CSRF trusted origins |

## Frontend (React + Vite)

### Setup

```bash
cd frontend
npm install
npm run dev
```

The React app runs on `http://localhost:5173` and proxies `/api` requests to the Django backend.

### Pages

- `/` — Product listing with category filter
- `/product/:id/:slug` — Product detail + add to cart
- `/cart` — Shopping cart
- `/checkout` — Order checkout form
- `/login` — Login
- `/register` — Register
- `/profile` — User profile (authenticated)
- `/orders` — Order history (authenticated)
- `/orders/:id` — Order detail (authenticated)
