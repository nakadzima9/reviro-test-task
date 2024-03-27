# Reviro Test Task API
____
**It's Django REST application for "Reviro Internship Tech Start Spring - 2024"**

## Installation
____
1. **Install [poetry](https://python-poetry.org/docs/#installation) package manager** 
2. **Clone the repository and go to the project directory:**

```
https://github.com/nakadzima9/reviro-test-task.git
cd reviro-test-task
```
3. **Install dependencies with poetry:**
```
poetry install --no-root
```
4. **Activate python virtaul environment**
```
poetry shell
```

## Env file configration
____
Create .env file and fill data. Use my **.env-example** file for e.g.
```commandline
DEBUG=True
SECRET_KEY='YOUR-SECRET-KEY'
ALLOWED_HOSTS=127.0.0.1, 0.0.0.0
DATABASE_URL=postgres://PG_USER:PG_PASSWORD@db:5432/PG_DB
```

## Usage
____
1. **Run the application using docker-compose**
```commandline
docker-compose up -d --build
```
2. **Migrate database the new PostgreSQL, execute the following command.**
```commandline
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
3. **If you wanted to run createsuperuser so:**
```
docker-compose exec web python manage.py createsuperuser
```
4. **Running unittests**
```
docker-compose exec web python manage.py test
```

## How to user API
____ 
**To use Swagger:**
- Follow the link http://127.0.0.1:8000/ in your web browser after launching the application
- You will see a list of all available endpoints, grouped by resources (for example, products, companies).
- Click on any endpoint to expand it and view detailed information, including the HTTP method, parameters, request body schema, and responses.
- To try out the endpoint, click the "Try" button, fill in all the necessary parameters or query text and click "Run". Swagger will send a request to your API and display the response directly in the user interface.
- This makes it easy to test the functionality of your API without the need for additional tools such as Postman or curl.

## Licence
____
[GPLv3](https://www.gnu.org/licenses/)