# kanyai

KanyAI NLG

### Local testing

Due to the Google Cloud logging, an environment variable 

To get a key:
 - Go to https://console.cloud.google.com/iam-admin/serviceaccounts?project=kanyai
 - Download a key for  kanyai@appspot.gserviceaccount.com
 - Save it in ./secrets (don't upload it to Github!)
 - Set an env variable GOOGLE_APPLICATION_CREDENTIALS=./secrets/<keyfile>.json

### Tests (run during pipeline)

flake8 style enforcement:

`flake8 --ignore=E203,C901,E402,E501,D400 --max-line-length=160 src/ test/ app.py`

Bandit security linting:

`bandit app.py`

Pytest unit tests with 80% minimum coverage:

`python3 -m pytest --cov=src --cov-fail-under=80`

### Deployment (run during merge to master)
`gcloud app deploy`

###Run locally
```
export GOOGLE_APPLICATION_CREDENTIALS=./secrets/kanyai-7efdbd925a1f.json
gunicorn app:app
```

### Build/Run Docker Container
```bash
# Build the container
docker build -t kanyai .

# Run and expose port 8080
docker run -it -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS=kanyai-7efdbd925a1f.json kanyai:latest
```

