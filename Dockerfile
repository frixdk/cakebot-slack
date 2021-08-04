FROM python:3

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

CMD ["./docker-entrypoint.sh"]