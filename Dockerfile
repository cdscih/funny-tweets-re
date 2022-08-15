FROM python:3.9-slim AS BUILD
ARG POETRY_VERSION=1.1.13
RUN apt-get update && \
  apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  python3 -m venv /venv && \
  /venv/bin/pip install --upgrade pip setuptools wheel && \
  /venv/bin/pip install "poetry==${POETRY_VERSION}"

# non-dev only dependencies export https://github.com/python-poetry/poetry/issues/1441#issuecomment-1140246353
RUN curl -sSL https://install.python-poetry.org | python - --git https://github.com/python-poetry/poetry.git@master \
  poetry plugin add poetry-plugin-export

COPY pyproject.toml poetry.lock /
RUN /venv/bin/poetry export --with-credentials --format requirements.txt --output /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM mcr.microsoft.com/vscode/devcontainers/python:3.9-bullseye as DEV
COPY --from=BUILD /venv /venv
ENV PATH=/venv/bin:$PATH

RUN apt-get update; \
  apt-get install -y --no-install-recommends zip vim docker.io curl gcc g++ libsasl2-dev; \
  rm -rf /var/lib/apt/lists/*; \
  poetry config virtualenvs.create false;

RUN curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
  chmod +x /usr/local/bin/docker-compose

FROM python:3.9-slim as PROD
COPY --from=BUILD /venv/lib/python3.9/ /usr/local/lib/python3.9/

COPY src/ src/

CMD ["python", "src/main.py"]