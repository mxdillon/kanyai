FROM python:onbuild

ENV PORT 8080
EXPOSE 8080

COPY requirements.txt app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=2", "main:app"]
