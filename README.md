# kanyAI

[kanyAI](https://www.kanyai.com/) lyric generator created by [mxdillon](https://github.com/mxdillon) & [j-penson](https://github.com/j-penson)

### Tests (run during pipeline)

flake8 style enforcement:

`flake8 --ignore=E203,C901,E402,E501,D400 --max-line-length=160 src/ test/ app.py`

Pytest unit tests with 80% minimum coverage:

`python3 -m pytest --cov=src --cov-fail-under=80`


### Model



### Run locally
```

pip install functions-framework

cd ./kanyai-function

export GOOGLE_APPLICATION_CREDENTUALS=../secrets/...

functions-framework --target get_lyrics --port 8081

curl http://localhost:8081 --form 'text_input=test

```
