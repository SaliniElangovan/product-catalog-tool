from db import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))

    attributes = db.relationship("Attribute", backref="category", cascade="all, delete-orphan")
    products = db.relationship("Product", backref="category", cascade="all, delete-orphan")

class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.String(20), nullable=False)  # text, number, decimal, boolean, date, enum
    options = db.Column(db.String(255))  # comma-separated values for enum
    is_required = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    attribute_values = db.relationship("ProductAttributeValue", backref="product", cascade="all, delete-orphan")

class ProductAttributeValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id"), nullable=False)

    value_text = db.Column(db.String(255))
    value_number = db.Column(db.Integer)
    value_decimal = db.Column(db.Float)
    value_boolean = db.Column(db.Boolean)
    value_date = db.Column(db.Date)

    attribute = db.relationship("Attribute")

    def set_value(self, value):
        if self.attribute.data_type == "text":
            self.value_text = value
        elif self.attribute.data_type == "number":
            self.value_number = int(value)
        elif self.attribute.data_type == "decimal":
            self.value_decimal = float(value)
        elif self.attribute.data_type == "boolean":
            self.value_boolean = (value.lower() == "true")
        elif self.attribute.data_type == "date":
            from datetime import datetime
            self.value_date = datetime.strptime(value, "%Y-%m-%d").date()
        elif self.attribute.data_type == "enum":
            if self.attribute.options and value in self.attribute.options.split(","):
                self.value_text = value
            else:
                raise ValueError("Invalid enum option")

    def get_value(self):
        return (
            self.value_text or
            self.value_number or
            self.value_decimal or
            self.value_boolean or
            self.value_date
        )
