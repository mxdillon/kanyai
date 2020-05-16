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
locust -f ./test/load/locustfile.py --host http://localhost:8080

# Run locust for 10 users, don't start the webUI and show a summary
locust -f ./test/load/locustfile.py --host http://localhost:8080 --clients 10 --no-web --only-summary --run-time 3m

```
