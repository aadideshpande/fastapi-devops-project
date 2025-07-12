# fastapi-devops-project

# Stock Trader FastAPI + Jenkins CI

A toy stock-trading API built with FastAPI, complete with a Jenkins pipeline.

## Prerequisites

- Python 3.8+
- pip
- Jenkins (with Git, Pipeline, AnsiColor, and Cobertura plugins)

## Setup

```bash
git clone git@github.com:aadideshpande/fastapi-devops-project.git
cd fastapi-devops-project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


```
uvicorn app.main:app --reload
http://localhost:8000/docs

```

## Tests & Coverage

Run all tests with:

```bash
coverage run -m unittest discover -s tests -p "test_*.py" && coverage report -m
coverage html
```

