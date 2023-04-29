# News Search Platform


## About
Simple interactive platform which internally uses [News API](https://newsapi.org/) to fetch News based on provided keywords.
To keep this application short and simple, I have used [jQuery](https://github.com/jquery/jquery) as frontend and [Django](https://github.com/django/django) with [DRF](https://github.com/encode/django-rest-framework) as backend. [Click here](docs/about.md) to know about implemetation.



## Installation

Following instructions are meant for Debian based Linux distro, but not limited to. I suggest you to find alternatives packages suitable your distro, especially for database server.


### Setup application server
- Install system packages.
```sh
sudo apt install virtualenv python3-dev python3-pip redis nginx
```
- Create virtual environment for backend server and activate same.
```sh
virtualenv -p python3 env
. env/bin/activate
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
- Ready static files
```sh
python manage.py collectstatic
```
- Run server.
```sh
python manage.py runserver localhost:8080
```

#### Async task:
- For async celery task, open new terminal and load same virtual environment:
```sh
. env/bin/activate
```

- Change directory to application code and call run celery application:
```sh
cd news_bl
celery -A news_bl worker -l INFO 
```

- You can add multiple workers for celery application by '--concurrency=2' option.


### Setup webserver
- Get your full path of frontend directory where index.html is resides and replace same with `__NEWS_INDEX_ROOT__` in conf/etc/nginx/sites-available/news.conf file.
- Copy news.conf congifuration to nginx's configuration directory
```sh
sudo cp conf/etc/nginx/sites-available/news.conf /etc/nginx/sites-available/default
```
- Link that file in sites-enable context
```sh
sudo ln -s conf/etc/nginx/sites-available/default /etc/nginx/sites-enabled/
```
- Text nginx configuration
```sh
sudo nginx -t
```
- Restart nginx service
```sh
sudo service nginx restart
```