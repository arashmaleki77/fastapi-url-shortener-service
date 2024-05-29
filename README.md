# URL Shortener Service

URL Shortener Service is using Fast Api. It allows users to create and view their shortener urls. 
It uses PostgresSQL as its database management system and Redis to cash redirect api for better performance.

This Service has been personalized for user. that means each user has a sub_directory for itself and users can share a 5 length chars of short_url

Each short_url contain digits and lower case and upper case characters. 
short_url and user_id are unique together so with growth of users, 5 length chars of short_urls are not going to be finished. So all short urls can remain forever.

Maximum limit of short_url for each user is 916,132,832 (62^5)

This service is needed a reliable, scalable and consistent database.  Postgresql is use ACID properties and with sharding it is a good choice for future needs like having a dashboard for users and selling premium account and analytics for their urls and strong search and filters or other features.

Redirect url has a huge amount of load and this problem simply can be solved with cashing url for something like 3 hours in Redis.

Fast api is very light, and it handles async.

This service use py_jwt for authenticate users.

## Getting Started

### Doc

Swagger URL after running back-end-service: `<BACK_END_SERVICE_URL>/docs`

### Prerequisites

Before running the project, you'll need to have the following installed on your machine:

- Python 3
- PostgreSQL
- Redis
- Docker (if running with Docker)

### Environment Variables

This project uses environment variables to store sensitive information such as database credentials. To run the project, you'll need to create a `.env` file in the root directory of your project and add the required variables just like `.env.sample` file.

1. Create a `.env` file in the root directory of your project:

```bash
touch .env
```

2. Open the `.env.sample` file and copy its contents, paste the contents of the `.env.sample` file into the `.env` file.

3. Replace the default values of the variables with your own values.

```
POSTGRES_USER=<your_postgres_username>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_DB=<your_database_name>
POSTGRES_HOST=<your_database_host>
POSTGRES_PORT=<your_database_port>

DEBUG=False
SECRET_KEY='<SECRET_KEY>'
REDIS_HOST="localhost"
REDIS_PORT=6379

JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="60"

FRONT_END_URL="<FRONT_END_URL>"
```

Save the `.env` file.

### Running Locally

To run the project locally, follow these steps:

1. Ensure that PostgreSQL is installed and running locally.
2. Clone the repository to your local machine:

```bash
cd fastapi-url-shortener-service/
```

3. Install the project's dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. CreateDb:
```bash
python create_db.py
```

5. Apply the migrations:

````bash
alembic upgrade head
````

6. Run the development server:

````bash
fastapi dev main.py
````
Once the server is running, you can access the API at http://localhost:8000/.

### Running with Docker

To run the project using Docker, follow these steps:

1. Clone the repository to your local machine:

```bash
cd fastapi-url-shortener-service/
```

2. Build and start the Docker containers:

````bash
docker-compose build
docker-compose --env-file=.env up -d
````

Once the containers are running, you can access the API at http://localhost:5000/.

#### Running Tests

To run the tests, follow these steps:

1. Activate the virtual environment:

```bash
source venv/bin/activate
```

2. Ensure that the project's dependencies are installed:

```bash
pip install -r requirements.txt
```

3. CreateDb:
```bash
python create_db.py
```

4. Run the tests:

```
pytest
```

This will run all the tests in the project.

Once the tests have completed running, you should see a summary of the test results in your terminal.
