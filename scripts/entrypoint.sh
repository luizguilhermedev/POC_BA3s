gunicorn src.server:app --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:6543 --reload --timeout 300 --log-level debug