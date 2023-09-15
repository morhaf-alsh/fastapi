FROM python:latest

WORKDIR app

COPY . .

VOLUME ./data ./data

RUN pip install -r requirement.txt

CMD ["uvicorn", "hello:app", "--reload", "--host", "0.0.0.0"]

EXPOSE 8000