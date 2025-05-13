# Playwright UI Testing Project

This project contains UI tests using Playwright for Python.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

To run all tests:
```bash

```

To run tests with UI:
```bash
pytest 
```

To run tests in a specific browser:
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
``` 

```bash
| call                                       | explanation |
| pytest                                     | All |
| tests/test_example.py                      | Run a specific test file|
| tests/test_example.py::test_homepage_title |Run a specific test function|
| --headed                                   |run tests with UI|
| -k "homepage"                              |Run tests matching a pattern|

```
