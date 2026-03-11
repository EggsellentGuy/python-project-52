install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

start:
	uv run python manage.py runserver 0.0.0.0:8000

start-server:
	uv run python manage.py runserver 0.0.0.0:3000

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	uv run pytest

test-coverage:
	uv run pytest task_manager --cov=task_manager --cov-report=xml:coverage.xml