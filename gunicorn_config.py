import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
# Keep workers low per pod and scale horizontally via Deployment replicas / HPA.
# Each worker is a full Python process, so memory cost grows linearly; the pod's
# CPU request should roughly match this number.
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")
# Recycle workers periodically to bound memory growth from leaks / fragmentation.
# Jitter avoids all workers restarting simultaneously.
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "100"))
