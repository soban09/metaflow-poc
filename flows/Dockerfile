FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    g++ \
    gfortran \
    openblas-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./ /app/

CMD ["python", "machinelearningflow.py", "run"]