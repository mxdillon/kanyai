FROM python:onbuild
COPY requirements.txt .
ENV PORT 8080
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
