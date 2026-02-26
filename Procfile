release: python backend/manage.py migrate && python backend/manage.py collectstatic --noinput
web: gunicorn --chdir backend ecommerce.wsgi
