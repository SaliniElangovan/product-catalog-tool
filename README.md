# Product Management Tool

Internal tool to manage product categories, attributes, and products with **category-specific attributes**.

---

## Features
- Manage **Categories** (create, view, delete)  
- Define **Attributes per Category**:
  - Supported types: `text`, `number`, `decimal`, `boolean`, `date`, `enum`
  - Enum attributes allow defining custom options (e.g., Gender → Male/Female)
  - Attributes can be marked as **required** or optional  
- Create **Products**:
  - Each product belongs to a category
  - Products automatically show only that category’s attributes
  - Fill attribute values based on their type (dynamic form fields)
- Manage **Product Attribute Values** (stored per product-attribute pair)
- Full **CRUD support** for categories, attributes, and products
- SQLite backend by default (can be switched to Postgres/MySQL easily)
- Flask + SQLAlchemy backend with Bootstrap-based UI  

---

## Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

# 4. Run the server
flask run --debug
