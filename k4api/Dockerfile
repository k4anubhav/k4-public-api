FROM python:3.12.3-alpine AS builder

ENV PATH="/venv/bin:$PATH"
RUN pip install virtualenv
RUN virtualenv --seeder pip /venv

RUN pip install --upgrade pip

RUN apk update && apk add --no-cache git

COPY ./requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.12.3-alpine AS release

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install gunicorn==23.0.0


COPY . /app

RUN ls .

WORKDIR /app/

RUN mkdir -p /app/static
RUN mkdir -p /app/media
RUN mkdir -p /app/logs
RUN mkdir -p /app/data

ENV PORT 8080
EXPOSE 8080

CMD exec gunicorn --config '/app/conf/gunicorn_conf_docker.py' app.wsgi:application