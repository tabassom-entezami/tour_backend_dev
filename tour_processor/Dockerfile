# syntax = docker/dockerfile:1.2

# Stage 1: Tour base
FROM python:3.7-slim-buster as base
RUN apt-get update && \
    apt-get install --no-install-recommends --yes curl netcat libpq-dev
RUN pip install --upgrade pip pip-tools
RUN mkdir /app

# Stage 2: Tour builder
FROM base as builder
RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --yes --no-install-recommends \
    build-essential autoconf automake libtool pkg-config libc++-dev git libffi-dev
ARG ENV=dev
ARG PYPI_ADDRESS
COPY requirements /app/requirements
COPY setup.py /app
RUN --mount=type=cache,target=/root/.cache \
    cd /app && \
    if [ "$ENV" = dev ]; then \
        pip install -i ${PYPI_ADDRESS} --extra-index-url https://pypi.org/simple \
        -r requirements/requirements.txt -r requirements/requirements-dev.txt -e .; \
    else \
        pip install -i ${PYPI_ADDRESS} --extra-index-url https://pypi.org/simple \
        -r requirements/requirements.txt .; \
    fi
RUN apt-get install -y python-tk

# Stage 3: Tour app image
FROM base
RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --yes --no-install-recommends libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 libgomp1 libgtk2.0-0
COPY --from=builder /usr/local /usr/local
COPY . /app
RUN chmod +x /app/run.sh
WORKDIR /app
EXPOSE 3000
CMD ["/app/run.sh"]
