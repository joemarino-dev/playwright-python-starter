# Playwright Test Automation - UI & API

Demonstrates comprehensive test automation using Playwright with Python and pytest for both UI and API testing.

## What This Shows

- **UI Testing**: Browser automation with semantic locators
- **API Testing**: REST API validation using Playwright's request context
- pytest fixtures for test setup/teardown
- Clean test organization by test type
- Assertion best practices

## Setup

Create and activate a virtual environment:

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

## Run Tests

**Run all tests:**
```bash
pytest
```

**Run only UI tests:**
```bash
pytest tests/ui/
```

**Run only API tests:**
```bash
pytest tests/api/
```

## Test Coverage

### UI Tests (tests/ui/)
- **test_title.py**: Validates page title
- **test_heading.py**: Validates heading text using semantic locators
- **test_body.py**: Validates body content

### API Tests (tests/api/)
- **test_get_user.py**: Validates GET request and user data structure
- **test_get_single_post.py**: Validates single resource retrieval
- **test_create_post.py**: Validates POST request and response structure

## Key Features

- Separate fixtures for UI (`page`) and `api_request_context`) testing
- Modular test organization
- Demonstrates Playwright's unified testing capabilities