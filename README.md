# kanyai

KanyAI lyric generator


### Tox
- license attribution
- flake8 style enforcement
- bandit security linting
- pytest unit tests with 80% minimum coverage

### Docker testing
```bash
# Build the container
docker build -t kanyai .

# Run and expose port 8080
docker run -it -p 8080:8080 kanyai
```

