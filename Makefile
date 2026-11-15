build:
	./build.sh

setup: install collectstatic migrate

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

dev:
	uv run manage.py runserver