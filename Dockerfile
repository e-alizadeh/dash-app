FROM python:3.8

COPY deploy-env.txt /
RUN pip install -r /deploy-env.txt

RUN mkdir /app
COPY ./app/ /app/

WORKDIR /app
CMD ["python", "app.py"]

