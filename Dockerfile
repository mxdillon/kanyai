FROM tensorflow/tensorflow:1.15.0-py3

ENV PORT 8080
EXPOSE 8080

COPY requirements.txt app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=1", "main:app"]
