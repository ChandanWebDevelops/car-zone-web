# 🚗 AutoMarket - Premium Car E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Stripe](https://img.shields.io/badge/Stripe-Payments-purple.svg)](https://stripe.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_15-blue.svg)](https://www.postgresql.org/)

A full-featured, production-ready car dealership e-commerce platform built with Django. It features a session-based shopping cart, real-time Stripe payment integration, a sleek responsive UI, and a fully containerized Docker architecture.

---

## 🚀 Setup & Installation Instructions

You can run this project using **Docker** (Recommended) or a **Local Python Environment**. 

### Prerequisites
- **Docker Method:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- **Local Method:** Python 3.13+, PostgreSQL 15+, and `pip`.

---

### Method 1: Docker Setup (Recommended & Easiest) 🐳

This method spins up the Django app and a PostgreSQL 15 database in isolated containers. No need to install Python or Postgres on your actual machine!

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/automarket.git
cd automarket
```

**2. Create your Environment Variables file:**
```bash
cp .env.example .env
```
*(Open `.env` in a text editor and add your Django `SECRET_KEY` and Stripe API keys. See the [Environment Variables](#-environment-variables) section below).*

**3. Build and start the containers:**
```bash
docker-compose up --build
```
> 💡 **Troubleshooting Docker:** If you get an error saying *"database files are incompatible with server"*, it means you have an old Postgres volume. Run `docker-compose down -v` to delete the old volume, then run `docker-compose up --build` again.

**4. Seed the database with sample cars:**
Open a **new terminal window** (keep the first one running the server) and run:
```bash
docker-compose exec web python manage.py seed_cars
```

**5. Create an Admin Superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

**6. View the App:**
- **Homepage:** [http://localhost:8000](http://localhost:8000)
- **Admin Panel:** [http://localhost:8000/admin](http://localhost:8000/admin)

---

### Method 2: Local Setup (Without Docker) 💻

If you prefer to run the app directly on your machine.

**1. Clone and navigate to the project:**
```bash
git clone https://github.com/yourusername/automarket.git
cd automarket
```

**2. Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up the PostgreSQL Database:**
Open your PostgreSQL shell (`psql`) and run:
```sql
CREATE DATABASE automarket;
CREATE USER automarket WITH PASSWORD 'automarket';
ALTER ROLE automarket SET client_encoding TO 'utf8';
ALTER ROLE automarket SET default_transaction_isolation TO 'read committed';
ALTER ROLE automarket SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE automarket TO automarket;
```

**5. Configure your `.env` file:**
Create a file named `.env` in the root directory and add your keys:
```env
SECRET_KEY=your-super-secret-django-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
POSTGRES_DB=automarket
POSTGRES_USER=automarket
POSTGRES_PASSWORD=automarket
```

**6. Apply migrations, seed data, and run:**
```bash
python manage.py migrate
python manage.py seed_cars
python manage.py createsuperuser
python manage.py runserver
```
Visit [http://localhost:8000](http://localhost:8000) in your browser!

---

## 🔐 Environment Variables

The project uses `python-decouple` to manage secrets. Create a `.env` file in the root directory based on `.env.example`:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key (generate a new one for production) |
| `DEBUG` | Set to `1` for local, `0` for production |
| `ALLOWED_HOSTS` | Comma-separated list of domains (e.g., `localhost,127.0.0.1`) |
| `STRIPE_PUBLISHABLE_KEY` | Your Stripe public test key (`pk_test_...`) |
| `STRIPE_SECRET_KEY` | Your Stripe secret test key (`sk_test_...`) |
| `POSTGRES_DB` | Database name (default: `automarket`) |
| `POSTGRES_USER` | Database user (default: `automarket`) |
| `POSTGRES_PASSWORD` | Database password (default: `automarket`) |

---

## 💳 Testing Stripe Payments

The app is configured to use Stripe's **Test Mode**. When checking out, use these magic card details:

**✅ To simulate a SUCCESSFUL payment:**
- **Card Number:** `4242 4242 4242 4242`
- **Expiration:** Any future date (e.g., `12/28`)
- **CVC:** Any 3 digits (e.g., `123`)
- **Zip Code:** Any 5 digits (e.g., `12345`)

**❌ To simulate a DECLINED payment:**
- **Card Number:** `4000 0000 0000 0002`

---

## 🛠️ Tech Stack

- **Backend:** Django 6.0, Python 3.13
- **Database:** PostgreSQL 15
- **Frontend:** Bootstrap 5, HTML5, CSS3, FontAwesome
- **Payments:** Stripe Checkout API
- **Server:** Gunicorn (Production), Django Dev Server (Local)
- **DevOps:** Docker, Docker Compose
- **Admin UI:** Django Jazzmin (Dark Mode)

---

## 📁 Project Structure

```text
automarket/
├── config/                 # Django project settings & routing
├── store/                  # Main e-commerce application
│   ├── management/         # Custom commands (seed_cars)
│   ├── models.py           # Car, Order, OrderItem models
│   ├── views.py            # Cart, Checkout, and Payment logic
│   ├── cart.py             # Session-based shopping cart class
│   └── forms.py            # Checkout and Auth forms
├── templates/              # Bootstrap 5 HTML templates
├── static/                 # Custom CSS, JS, and Images
├── Dockerfile              # Python container configuration
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Python dependencies
└── manage.py               # Django CLI entry point
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---
*Built with ❤️ and a lot of ☕ using Django & Docker.*
