FROM python:onbuild
COPY requirements.txt .
ENV PORT 80
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]
