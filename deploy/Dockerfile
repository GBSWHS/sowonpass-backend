FROM alpine:3.18 as builder
ARG PYTHON_VERSION=3.11

RUN apk add --update --no-cache python3 py3-pip
RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY pyproject.toml poetry.lock alembic.ini /app/
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY sowonpass_backend/ /app/sowonpass_backend/
RUN poetry build && pip install --no-cache-dir dist/*.whl
RUN rm -rf dist sowonpass_backend

WORKDIR /usr/lib/python${PYTHON_VERSION}/site-packages
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'pip*' -exec rm -rf {} +
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'setuptools*' -exec rm -rf {} +
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'virtualenv*' -exec rm -rf {} +
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'watchfiles*' -exec rm -rf {} +
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'installer*' -exec rm -rf {} +
RUN find . -mindepth 1 -maxdepth 1 -type d -name 'poetry*' -exec rm -rf {} +
RUN test -f distutils-precedence.pth && rm distutils-precedence.pth || true

WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN rm -rf ensurepip venv
RUN python3 -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

FROM scratch as prod
ARG PYTHON_VERSION=3.11

COPY --from=builder /usr/bin/python3 /

COPY --from=builder /lib/libz.so.1 /lib/
COPY --from=builder /lib/ld-musl-x86_64.so.1 /lib/
COPY --from=builder /usr/lib/libssl.so.3 /usr/lib/
COPY --from=builder /usr/lib/libcrypto.so.3 /usr/lib/
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/

COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/

WORKDIR /app
COPY --from=builder /app/ /app/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/site-packages/sowonpass_backend/ /app/sowonpass_backend/

CMD ["/python3", "-m", "sowonpass_backend"]

FROM alpine:3.18 as dev
ARG PYTHON_VERSION=3.11

#RUN apk update \
#    && apk add --virtual build-deps gcc python3-dev py3-pip musl-dev \
#    && apk add --no-cache mariadb-dev
RUN apk add --update --no-cache python3 py3-pip
RUN pip install --no-cache-dir poetry

RUN cp /usr/bin/python3 /

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install

COPY . /app/
RUN poetry build && pip install --no-cache-dir dist/*.whl

CMD ["python3", "-m", "sowonpass_backend"]
