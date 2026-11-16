build-css:
	uv run python manage.py tailwind build --force

setup: install build-css collectstatic migrate

dev:
	uv run python manage.py tailwind runserver
render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput --ignore source.css

migrate:
	uv run python manage.py migrate