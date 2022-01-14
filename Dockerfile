# Dockerfile
## Build venv
FROM python:3.9 AS venv

ENV POETRY_VERSION=1.2.1
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# The `--copies` option tells `venv` to copy libs and binaries
# instead of using links (which could break since we will
# extract the virtualenv from this image)
RUN python -m venv --copies /app/venv
RUN . /app/venv/bin/activate && pip install poetry && poetry install


## Beginning of runtime image
# Remember to use the same python version
# and the same base distro as the venv image
FROM python:3.9-alpine3.14 as prod

COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH

WORKDIR /app
COPY . ./

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8080', timeout=2)"

CMD ["uvicorn", "src.server:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]