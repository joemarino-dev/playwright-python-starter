# Playwright Python Starter

![Tests](https://github.com/joemarino-dev/playwright-python-starter/actions/workflows/tests.yml/badge.svg)

Comprehensive test automation framework demonstrating UI, API, and integration testing with Python, Playwright, and pytest. Features automated CI/CD pipeline with GitHub Actions.

## What This Demonstrates

- **UI Testing**: Browser automation with Playwright and semantic locators
- **API Testing**: REST API validation using Playwright's request context
- **Integration Testing**: End-to-end tests combining UI, API, and database validation
- **Property-Based Testing**: Validating business rules that must always hold true
- **CI/CD Pipeline**: Automated test execution via GitHub Actions on every commit
- **Clean Architecture**: Modular test organization with reusable pytest fixtures

## Setup

Create and activate a virtual environment:

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
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
```bash
pytest                  # Run all tests
pytest tests/ui/        # Run only UI tests
pytest tests/api/       # Run only API tests
pytest tests/integration/  # Run only integration tests
```

## Test Coverage

### UI Tests (`tests/ui/`)
- Page title validation
- Heading text validation using semantic locators
- Body content validation

### API Tests (`tests/api/`)
- GET request validation with data structure assertions
- Single resource retrieval
- POST request validation

### Integration Test (`tests/integration/test_transfer_e2e.py`)
End-to-end banking transfer test combining:
- UI interaction (Playwright form submission)
- API processing (Flask transfer endpoint)
- Database verification (SQL balance validation)
- Property validation (conservation of money across accounts)

Demonstrates full-stack testing workflow: UI → API → Database → Verification

## CI/CD

GitHub Actions automatically runs all tests on every push. View the [workflow file](.github/workflows/tests.yml) for configuration details.