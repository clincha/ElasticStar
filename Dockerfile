FROM python

COPY requirements.txt .

RUN python -m pip install daphne

RUN python -m pip install -r requirements.txt

COPY ElasticStar /app

WORKDIR /app


WORKDIR /app

EXPOSE 8000

RUN manage.py migrate

ENTRYPOINT python -m daphne -b 0.0.0.0 -p 8000 ElasticStar.asgi:application