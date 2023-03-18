# Let's Make a ML Experiment Tracking

This article shows you how to streamline your machine learning workflow with a custom experiment tracker.
Photo by Ousa Chea on Unsplash(This article is a demonstration of my side project and its not intended for production use please consult a expert if you wish to use something that tracks your machine learning projects.)

[Just want to see some source code? My pleasure: https://github.com/Joel-hanson/model-tracker]

## Introduction

This blog will show you how to make something that will help us keep track of your machine learning experiments. When I was working on a project that needed to train and deploy machine learning models that use autoML packages and require the least amount of work from a user, I came across this idea.

We would only look at the part of that project that has to do with tracking experiments, not the whole model lifecycle. This is not meant to be used in production; it's just a sample project. For tracking, logging, and querying experiments, I suggest using a mlflow which is a open source platform to manage the machine learning lifecycle.

This article is for people who already know the basics about Python and its packages, such as Django and Celery. For the project, I'll be using Docker, and the code for the project is in the github repo.

## Problem statement

This article showcases how you can use a django Celery project to do end-to-end workflow for a machine learning model. The problem statement is to build a project that would help us in keeping track of our machine learning experiments. The project should be able to do the following:

1. Create a new experiment
1. Run the experiment
1. Track the experiment
1. Store the experiment results

## Solution

The solution that I have came up with is to make use of the django celery result. So what is django celery result? It is a django app that provides a database backend for storing the results of asynchronous tasks. It is a drop-in replacement for the default database backend that ships with Celery. It is a good idea to use this app if you want to store and query the results of your tasks in the database.

The solution will be broken down into the following subsections:

1. Prerequisites
1. Setup the project
1. Run the project
1. Create a new experiment

## Prerequisites

1. Python 3.8.5
1. Docker
1. Docker compose
1. Postgres
1. Redis

## Setup the project

I am going to be using a docker container to run my project. I have created a docker file that will be used to build the image for the project. The docker file is as follows:

```dockerfile
FROM python:3.8.5

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/
```

In order to use the docker file we need to create a docker compose file. The docker compose file is as follows:

```dockerfile
version: "3.9"
services:
  redis: # This for storing cache
    image: "redis:alpine"
    hostname: redis
    ports:
      - 6379:6379
    logging:
        driver: none

  db:
    image: postgres:12-alpine
    volumes:
      - ./db:/var/lib/postgresql/data
    env_file:
      - backend/.env
    ports:
      - 5432:5432
    logging:
        driver: none

  backend:  # This service that serves the api for regression and classification
    build: backend
    entrypoint: ./entrypoint.sh
    image: app-backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - backend/.env
    depends_on:
      - db
      - redis
    stdin_open: true # for testing
    tty: true # for testing
```

The docker compose file is pretty straight forward. It has three services. The first service is the redis service. This service is used to store the cache. The second service is the database service. This service is used to store the data. The third service is the backend service. This service is used to serve the api for the project. The backend service depends on the database and the redis service. The backend service also has a entrypoint script that will be used to run the project. The entrypoint script is as follows:

```bash
#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
make migrate

# Start server
echo "Starting server"
make run
```

In the entrypoint script. It will apply the database migrations and then start the server. The entrypoint script is located in the backend directory. The backend directory is as follows:

```bash
├── .env
├── Dockerfile
├── Makefile
├── backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog.md
├── common
│   ├── __init__.py
│   ├── context_processors.py
│   ├── management
│   │   ├── __init__.py
│   │   └── commands
│   │       ├── __init__.py
│   │       └── celery.py
│   ├── models.py
│   ├── routes.py
│   ├── tasks.py
│   ├── urls.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── tests.py
│   └── views.py
├── entrypoint.sh
├── experiment
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── templatetags
│   │   ├── __init__.py
│   │   └── get_item.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── manage.py
├── requirements.txt
└── templates
    ├── _base.html
    ├── index.html
    └── result.html
```

The files Makefile, Dockerfile, entrypoint.sh, .env and requirements.txt are located in the backend directory.

1. Makefile: This file contains the commands that will be used to run the project.
1. Dockerfile: This file contains the instructions that will be used to build the image for the project.
1. entrypoint.sh: This file contains the commands that will be used to run the project.
1. .env: This file contains the environment variables that will be used to run the project.
1. requirements.txt: This file contains the dependencies that will be used to run the project.

**Note:** The .env file is not included in the repository. You will have to create the .env file yourself. The .env file is as follows:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
REDIS_URL=redis://redis:6379/0
```

The backend directory has the following subdirectories:

1. backend
2. common
3. experiment

The backend directory contains the django project files. The common directory contains the celery tasks and the celery worker. The experiment directory contains the models, serializers, views and urls for the project. The experiment directory also contains the django app for the project.

The common directory contains the common code for the project. The experiment directory contains the code for the experiment app. The backend directory contains the django settings, urls, wsgi and asgi files. It also has the celery.py file that is used to configure the celery app. The experiment directory has the following subdirectories:

1. migrations: This directory contains the migrations for the models.
1. templatetags: This directory contains the custom template tags.
1. utils: This directory contains the utils for the project.
1. routes: This file contains the routes for the app.
1. tasks: This file contains the celery tasks for the app.
1. urls: This file contains the urls for the app.
1. views: This file contains the views for the app.
1. models: This file contains the models for the app.
1. serializers: This file contains the serializers for the app.
1. tests: This file contains the tests for the app.

The experiment app has the following subdirectories:

1. routes: This directory contains the routes for the app.
1. tasks: This directory contains the celery tasks for the app.
1. urls: This directory contains the urls for the app.
1. views: This directory contains the views for the app.
1. models: This file contains the models for the app.
1. serializers: This file contains the serializers for the app.
1. tests: This file contains the tests for the app.
1. utils: This file contains the utils for the app.

In order to run the project, we need to install the dependencies. The dependencies are as follows:

```bash
celery[redis]==5.2.7
dj-database-url==1.2.0 # connect to databases with url REVIEW: if not need
Django==4.1.5
django-celery-results==2.4.0
django-cors-headers==3.13.0 # cors header plugin
django-redis==5.2.0
django-storages==1.13.2 # Storage backend for django
djangorestframework==3.14.0
flower==1.2.0 # celery task visualizer
python-decouple==3.7 # Helper for django and environment variables
psutil==5.9.4 # process and system utilities
psycopg2-binary==2.9.5 # PostgreSQL database adapter for the Python
pandas==1.5.3 # data analysis and manipulation tool
scikit-learn==1.2.1 # machine learning in Python
```

The dependencies can be installed by running the following command:

```bash
pip install -r requirements.txt
```

## Run the project

The project can be run by running the following command:

```bash
docker-compose up
```

The project can be accessed at <http://localhost:8000>. The flower can be accessed at <http://localhost:5555>.

You could also run the project without docker. The project can be run by running the following command:

```bash
python manage.py runserver
```

You have to run the migrations before running the project. The migrations can be run by running the following command:

```bash
python manage.py makemigrations
python manage.py migrate
```

To run the celery worker, you have to run the following command:

```bash
celery -A common worker -l info
```

To run flower, you have to run the following command:

```bash
celery -A common flower
```

To make a superuser, you have to run the following command:

```bash
python manage.py createsuperuser
```

## Create a new experiment

In order to create a new experiment, you have to visit request to the /experiment/ or /tasks/ endpoint. This would list you the current project configured that is the wine quality.

On selecting that or getting that api you should be sending a POST request. The request should contain the input data in the body. The input data should be a json with the following format:

```json
{
    "alpha": <REPLACE WITH THE EXPERIMENT VALUE>,
    "l1_ratio": <REPLACE WITH THE EXPERIMENT VALUE>,
}
```

The input data should be a json with the following format:

```json
{
    "alpha": 0.1,
    "l1_ratio": 0.5,
}
```

The alpha and l1_ratio are the hyperparameters. The hyperparameters can be changed by changing the values in the input data.

After sending the request, you will get a response with the following format:

```json
{
    "task_id": "<TASK ID>",
    "task": "<TASK URL>",
}
```

The task_id is the id of the task. The task is the url of the task. The task can be used to get the status of the task and the result of the task.

A sample task result is as follows:

```json
{
    "task_id": "e6b0b5a0-8b1f-4b1f-9f9f-8f8f8f8f8f8f",
    "status": "SUCCESS",
    "result": {
        "alpha": 0.1,
        "l1_ratio": 0.5,
        "rmse": 0.5,
        "mae": 0.5,
        "r2": 0.5,
        "date": "2023-03-18T12:00:00Z",
        "request_id": "e6b0b5a0-8b1f-4b1f-9f9f-8f8f8f8f8f8f"
    }
}
```

The task list can be found at <http://localhost:8000/experiment/wine-quality/tasks/>.

I have create a html with api's created in the project. The html can be found at <http://localhost:8000/results>. Also the task list can be found at <http://localhost:8000/>.

## Conclusion

In this article, we have created a django project that can be used to create experiments. The project can be used to task experiments for machine learning models. This can also be used to create experiments for other models, with different hyperparameters, etc... The scope goes on. The results can be stored in the database and can be used for future analysis. The results can be used to create dashboards and visualizations.

The project can be found at <https://github.com/Joel-hanson/model-tracker>
