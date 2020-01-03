# kanyai

KanyAI lyric generator


### Tests (run during pipeline)

flake8 style enforcement:

`flake8 --ignore=E203,C901,E402,E501,D400 --max-line-length=160 src/ test/ app.py`

Bandit security linting:

`bandit app.py`

Pytest unit tests with 80% minimum coverage:

`python3 -m pytest --cov=src --cov-fail-under=80`

### Deployment (run during merge to master)
`gcloud app deploy`


### Build/Run Docker Container
```bash
# Build the container
docker build -t kanyai .

# Run and expose port 8080
docker run -it -p 8080:8080 kanyai
```

