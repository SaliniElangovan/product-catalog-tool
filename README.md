# Product Catalog Tool

Internal tool to manage product categories, attributes, and products.

## Features
- Define categories and assign custom attributes
- Attribute types: text, number, decimal, boolean, date, enum
- Create products with dynamic category-specific attributes
- SQLite backend (switchable to Postgres/MySQL)
- Flask-based, simple UI

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
