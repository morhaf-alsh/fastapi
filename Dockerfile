FROM python:latest

WORKDIR app

COPY . .

RUN pip install -r requirement.txt

ENV DB_HOST="127.0.0.1"

ENV DB_PORT=306

ENV DB_USER="root"

ENV DB_PASSWD="root"

ENV DB_NAME="api"

CMD ["uvicorn", "hello:app", "--reload", "--host", "0.0.0.0"]

EXPOSE 8000