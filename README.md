# mossweb
Python/Django-based web GUI for Stanford's MOSS Similarity Checker

## Dependencies

### Django version 2.2.8

```
pip install Django==2.2.8
```

### mosspy 1.0.7

```
pip install mossy==1.0.7
```

### beautifulsoup4 4.7.1

```
pip install beautifulsoup4==4.7.1
```

## Installation

```
git clone https://github.com/julianowick/mossweb.git 
```

```
pip install -r mossweb/requirements.txt
```

You might want to create a local_settings.py file under the mossweb folder do personalize your installation. Some things you are likely to set:

```
SECRET_KEY = 'somegoodandsecretkey'
ALLOWED_HOSTS = ['yourhostname']
MOSS_USERID = 12345
UPLOADS_ROOT = '/your/upload/folder'
HTTP_PREFIX = 'mossweb/' # In case you are using a reverse proxy
STATIC_URL = '/mossweb/static/' # In case you set the HTTP_PREFIX
```

```
python manage.py migrate
```

```
python manage.py createsuperuser
```

```
python manage.py runserver 0.0.0.0:8000
```

Point your web browser to http://yourhost:8000/ and you should see the front page of the app. Use the Django admin module at http://yourhost:8000/admin to create courses and assignments.
