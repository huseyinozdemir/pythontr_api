The Api of Pythontr.com
==============

We develop pythontr_api for pythontr.com
-----------

Pythontr Api is a django rest api project

Development Notes:
---

Start project on docker-compose

Tips:
* docker-compose run app sh -c "django-admin.py startproject app ." # Create project
* docker-compose run app sh -c "python manage.py test && flake8" # Test
* docker-compose run app sh -c "python manage.py startapp core" # Create core
* docker-compose run app sh -c "python manage.py makemigrations" # Make migrations
