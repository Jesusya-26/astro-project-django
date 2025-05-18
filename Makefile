CODE := astrocat
PROJECT := astro_project

lint:
	poetry run pylint $(CODE)
	poetry run pylint $(PROJECT)

format:
	poetry run isort $(CODE)
	poetry run black $(CODE)
	poetry run isort $(PROJECT)
	poetry run black $(PROJECT)
run-server:
	poetry run python manage.py runserver

install:
	pip install .

install-dev:
	poetry install --with dev

install-dev-pip:
	pip install -e . --config-settings editable_mode=strict

clean:
	rm -rf ./dist

build:
	poetry build

install-from-build:
	python -m wheel install dist/idu_api-*.whl

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate