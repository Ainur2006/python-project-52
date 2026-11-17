.PHONY: install build-css collectstatic migrate setup dev build render-start test

install:
	uv sync

build-css:
	uv run python manage.py tailwind build --force

collectstatic:
	uv run python manage.py collectstatic --noinput --ignore source.css

migrate:
	uv run python manage.py migrate

setup: install build-css collectstatic migrate

dev:
	uv run python manage.py tailwind runserver

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

test:
	uv run python manage.py test