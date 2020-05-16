### Load Testing Notes

Load testing scripts

# Locust
Install Locust and dependency
```
brew install libenv

pip install locust
```

```
# Run locust and start the WebUI
locust -f ./test/load/locustfile.py --host https://europe-west2-kanyai.cloudfunctions.net/kanyai

# Run locust for 10 users, don't start the webUI and show a summary
locust -f ./test/load/locustfile.py --host https://europe-west2-kanyai.cloudfunctions.net/kanyai --clients 10 --no-web --only-summary --run-time 3m

```
