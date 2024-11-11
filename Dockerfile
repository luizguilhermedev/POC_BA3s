FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install additional dependencies for Python runtime
RUN pip install ipython langchain-experimental

COPY . .


COPY src/data /code/src/data

EXPOSE 8080


CMD ["streamlit", "run", "app.py", "--server.port", "8080"]

