# base image
FROM python:3.11

# install poetry
RUN pip install poetry

# set working directory
WORKDIR /app

# copy dependancies
COPY pyproject.toml poetry.lock /app/

# install dependancies
RUN poetry install

# copy everything else
COPY . /app

# instructions on how to run app
CMD ["poetry", "run", "python", "src/main.py"]

