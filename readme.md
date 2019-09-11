# Bus schedule

### Set environoment
    python -m venv venv
    souce venv/bin/activate
    python -m pip install -U pip
    pip install -r requirements.txt
### Edit settings.py database configuration
    DATABASES = {
            ...
            'NAME': 'yourdbname',
            'USER': 'yourdbuser',
            'PASSWORD': 'yourdbuserpassw',
            ...
            }
    }
#### Make application migrations
    python manage.py makemigrations schedule
    python manage.py migrate
### Load database dump
    psql -h localhost yourdbname yourdbuser < schedule.sql
### Run application
    python manage.py runserver
[localhost:8000/schedule](localhost:8000/schedule)
