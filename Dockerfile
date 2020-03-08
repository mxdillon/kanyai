FROM python:onbuild
COPY requirements.txt .
ENV PORT 80
EXPOSE 80
CMD ["gunicorn", "--bind=0.0.0.0:80", "--workers=5", "main:app"]
