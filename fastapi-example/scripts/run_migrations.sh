docker compose up

docker compose exec api uv run alembic revision --autogenerate -m "<your message>"

docker compose exec api uv run alembic upgrade head
