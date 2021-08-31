# News Search Platform

## About
Simple interactive platform which internally uses [News API](https://newsapi.org/) to fetch News based on provided keywords.
To keep this application short and simple, I have used [jQuery](https://github.com/jquery/jquery) as frontend and [Django](https://github.com/django/django) with [DRF](https://github.com/encode/django-rest-framework) as backend.

## Installation

Following instructions are meant for Debian based Linux distro, but not limited to. I suggest you to find alternatives packages suitable your distro, especially for database server.

### Setup application server
- Install system packages.
```sh
sudo apt install virtualenv python3-dev python3-pip redis nginx
```
- Create virtual environment for backend server and activate same.
```sh
virtualenv -p python3
```
- Install all required pip packages.
```sh
pip install -r news_search/conf/requirements.txt
```
- Ready database with admin user creation.
```sh
cd news_bl
python manage.py migrate
python manage.py createsuperuser
```
- Run server.
```sh
python manage.py runserver localhost:8080
```

### Setup webserver