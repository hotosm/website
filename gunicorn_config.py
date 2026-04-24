import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
workers = int(os.getenv("GUNICORN_WORKERS", "5"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")
