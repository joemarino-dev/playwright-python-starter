# Playwright + Pytest Starter (Python)
Small starter project to demonstrate:
- pytest fixtures via `conftest.py`
- Playwright UI assertions
- semantic locator usage (`get_by_role`)

## Setup
Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt
playwright install

## Run Tests
From the project root: 
pytest