FROM tensorflow/tensorflow:latest-py3

ENV PORT 80
EXPOSE 80

COPY requirements.txt app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["gunicorn", "--bind=0.0.0.0:80", "--workers=5", "main:app"]
