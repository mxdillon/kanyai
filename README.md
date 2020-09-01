# kanyAI

![CI-build](https://github.com/mxdillon/kanyai/workflows/CI-build/badge.svg)
![CD-build](https://github.com/mxdillon/kanyai/workflows/CD-build/badge.svg)

🎤 Use AI to generate Yandhi's next banger 🎤

Project is live at https://www.kanyai.com/. \
Created by [mxdillon](https://github.com/mxdillon) & [j-penson
](https://github.com/j-penson).

KanyAI is an implementation of GPT-2 trained on Yeezy's lyrics and interviews.

The model is served using Google Cloud Functions via [KanyUI])https://github.com/j-penson/kanyui), the React based front end.

If you look carefully in code, you might spot a hacky hack to get around the GCP function 2Gb memory limit ✌️

### Tests

flake8 style enforcement:

`flake8 --ignore=E203,C901,E402,E501,D400 --max-line-length=160 src/ test/ app.py`

Pytest unit tests with 80% minimum coverage:

`python3 -m pytest --cov=src --cov-fail-under=80`


### Local Dev Instructions

Test using pytest 
```
cd ./kanyai-function
export GOOGLE_APPLICATION_CREDENTUALS=../secrets/x.json

pytest
```



Run the function using [Functions Framework for Python](https://github.com/GoogleCloudPlatform/functions-framework-python)
```

# Activate the venv, set the env variable for GCP (replace x.json with secret name)
source ./env/bin/activate
cd ./kanyai-function
export GOOGLE_APPLICATION_CREDENTIALS=../secrets/x.json

# Install the framework
pip install functions-framework

# Run the framework
functions-framework --target get_lyrics --port 8081

# An example request
curl -X POST  http://localhost:8081 --form 'input=song about kim'

```
