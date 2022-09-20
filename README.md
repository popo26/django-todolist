# Family Calendar App

## What this app does:
This app allow you to add and remove your todo items as well as view the whole family calendar.
[Live site](https://whatsmyagendatoday.herokuapp.com/)

## Technology:
- Python 3
- Django
- HTML/CSS/SCSS
- Javascript

## Preparation for virtualenv, AWS S3 Bucket, and .env_example file:
1. Once clone or download this code, [create a virtualenv](https://docs.python.org/3/library/venv.html).
2. Acticate the virtualenv.
3. From terminal, install all the requirements with `pip install -r requirements.txt`.
4. I use [python-dotenv](https://pypi.org/project/python-dotenv/) to access environment variables.
5. Get a free API at [OpenWeather API](https://api.openweathermap.org). Fill related sections in the `.env_example` file.
6. Get a free API at [Nasa API](https://api.nasa.gov/). Fill related sections in the `.env_example` file.
7. Get a free API at [Rapid API](https://rapidapi.com/hub). Fill related sections in the `.env_example` file.
8. From terminal, run `python manage.py shell`. Then run following code to generate secret key.
    `from django.core.management.utils import get_random_secret_key`
    `print(get_random_secret_key())` --> Copy the key to SECRET_KEY in `.env_example`.
    `exit()`
9. rename `.env_example` to `.env`.


## Run the app:
1. From terminal, run below commands to launch the site, then go to `127.0.0.1:8000` in your browser.:
- `python manage.py migrate`
- `python manage.py runserver`



