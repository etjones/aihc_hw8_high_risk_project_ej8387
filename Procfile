redis: redis-server
tailwind: python adherence_web_app/manage.py tailwind start
web: python adherence_web_app/manage.py runserver
celeryworker: PYTHONPATH=adherence_web_app celery -A adherence_web_app.celery_app worker --loglevel=info
celerybeat: PYTHONPATH=adherence_web_app celery -A adherence_web_app.celery_app beat --loglevel=info
