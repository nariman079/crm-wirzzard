FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN pip install poetry
WORKDIR /crm/
COPY poetry.lock pyproject.toml /crm/
RUN poetry config virtualenvs.create false && poetry install
COPY ./app /crm/
