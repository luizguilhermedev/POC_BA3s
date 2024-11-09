FROM python:3.11 as requirements-stage

WORKDIR /tmp


RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11

WORKDIR /code
RUN apt update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
        build-essential \
        make \
        git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install uvicorn gunicorn

COPY . .

COPY ./src/data /code/data

RUN chmod +x scripts/entrypoint.sh

CMD exec ./scripts/entrypoint.sh

