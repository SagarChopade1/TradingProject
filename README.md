# TradingProject

## Requirements
- Python 3.10
- Pipenv
- Django
- Django REST Framework

### Clone the repo
### move into project directory
```
 cd TradingProject
```
### Activate environment:
```
pipenv shell
```
### Install dependencies:
```
pipenv install
```
### Database migration and superuser creation
```
python manage.py migrate
python manage.py createsuperuser --no-input
```
### Start the djnago server:
``` 
python manage.py runserver
```

## Access the API documentation at: http://localhost:8000/swagger/

