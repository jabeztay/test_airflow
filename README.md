# Airflow Test

Running Airflow 2.12 locally for testing.

## Description

Using [Docker](https://www.docker.com/) (and docker-compose) to setup an environment to test run Airflow.

The project currently covers
- Airflow 2.12 (Python 3.8) with Local Executor
- Source and target PostgresSQL database
- Simple DAG flow to extract data from source to target database
  - Including a simple data generator

## Usage

### Setup Details

Have both Docker and docker-compose installed and set up. Clone the repo and run the following
```bash
# create logs folder
mkdir logs
# initialises the Airflow database
docker-compose up airflow-init
# starts all the containers
docker-compose up -d
```

### Running the DAG
Visit localhost:5884 to access the Airflow UI, login using the credentials `airflow` for both username and password.

Start date for the DAG has been set to *1st August 2021*, change the date as needed, date set here was to have the DAG run for a few weeks as a test. Turn on the DAG after making required changes to the start date.

### Viewing the data

Data extracted from source to target can be viewed by running the following
```
docker exec -i test_airflow_target-db_1 psql -U target -d target -c "SELECT * FROM sales LIMIT 50"
```

Credentials set up for the Postgres target database are as defined in `docker-compose.yaml`
```
    environment:
      POSTGRES_USER: target
      POSTGRES_PASSWORD: target
      POSTGRES_DB: target
```