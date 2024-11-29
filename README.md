# The Api of Pythontr.com

## We develop pythontr_api for pythontr.com

Pythontr Api is a django rest api project

## Development Notes

Start project on docker-compose

Tips:

- docker-compose run app sh -c "django-admin.py startproject app ." # Create project
- docker-compose run app sh -c "python manage.py startapp core" # Create core
- docker-compose run app sh -c "python manage.py makemigrations" # Make migrations
- docker-compose run app sh -c "python manage.py createsuperuser" # Create superuser
- docker-compose run app sh -c "python manage.py test && flake8" # Test
- docker-compose run app sh -c "python manage.py collectstatic" # Create css ext.

## Git Hooks Install for quality check on codes

- chmod u+x scripts/install-hooks.sh
- sh scripts/install-hooks.sh

# exec: "docker-credential-desktop.exe": executable file not found in $PATH

- vim ~/.docker/config.json
- rename credsStore to credStore
