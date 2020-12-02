FROM python:3.8
RUN mkdir /app
COPY /application /app/application
COPY /config /app/config
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
ENV PYTHONPATH=${PWD} \
    CONFIG_PROFILE=default

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 3330
CMD uvicorn application.initializtion:app --host 0.0.0.0 --port ${PORT:-3330}

