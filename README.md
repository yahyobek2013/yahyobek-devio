# DEVIO

Django web studio website with services, portfolio, pricing, orders, authentication, and an admin dashboard.

## Local setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser.

The local SQLite database, uploaded media, and environment files are intentionally excluded from Git.
