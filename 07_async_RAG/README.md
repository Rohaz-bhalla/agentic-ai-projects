# To run this folder #

1. docker compose up -d (both valkey and qdrant)
2. uvicorn main:app --host 0.0.0.0 --port 8080 --reload
3. rq worker (separate integrated terminal)
