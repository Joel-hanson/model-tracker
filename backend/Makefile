run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell

test:
	python manage.py test

superuser:
	python manage.py createsuperuser

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "__pycache__" -exec rm -rf {} \;

reset:
	make clean
	rm -rf db.sqlite3
	make migrate
	make superuser
	make test


# Path: Makefile