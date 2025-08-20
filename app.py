from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----------------------
# MODELS
# ----------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    attributes = db.relationship("Attribute", backref="category", cascade="all, delete")


class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # text, number, boolean, enum
    options = db.Column(db.String(200))  # only used if enum
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category")
    attributes = db.relationship("ProductAttribute", backref="product", cascade="all, delete")


class ProductAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id"), nullable=False)
    value = db.Column(db.String(200))
    attribute = db.relationship("Attribute")


# ----------------------
# ROUTES
# ----------------------

@app.route("/")
def index():
    return redirect(url_for("products"))


# ---- Products ----
@app.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/products/new", methods=["GET", "POST"])
def product_form():
    categories = Category.query.all()
    if request.method == "POST":
        name = request.form["name"]
        sku = request.form["sku"]
        price_str = request.form.get("price", "0").strip()
        price = float(price_str) if price_str else 0.0
        category_id = request.form["category_id"]

        product = Product(name=name, sku=sku, price=price, category_id=category_id)
        db.session.add(product)
        db.session.commit()

        # Save attribute values
        for attr in Attribute.query.filter_by(category_id=category_id).all():
            val = request.form.get(f"attr_{attr.id}")
            if attr.data_type == "boolean":
                val = "true" if val == "true" else "false"
            if val is not None:
                db.session.add(ProductAttribute(product_id=product.id, attribute_id=attr.id, value=val))

        db.session.commit()
        return redirect(url_for("products"))

    return render_template("product_form.html", categories=categories)


@app.route("/products/delete/<int:id>", methods=["POST"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products"))


# ---- Categories ----
@app.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)


@app.route("/categories/new", methods=["GET", "POST"])
def new_category():
    if request.method == "POST":
        name = request.form["name"]
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("category_form.html")


# ---- Attributes ----
@app.route("/categories/<int:category_id>/attributes", methods=["GET", "POST"])
def manage_attributes(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        name = request.form["name"]
        data_type = request.form["data_type"]
        options = request.form.get("options")
        attr = Attribute(name=name, data_type=data_type, options=options, category=category)
        db.session.add(attr)
        db.session.commit()
        return redirect(url_for("manage_attributes", category_id=category_id))
    return render_template("attributes.html", category=category)


# ---- API Endpoint (for product_form.js) ----
@app.route("/api/categories/<int:category_id>/attributes")
def get_attributes(category_id):
    attrs = Attribute.query.filter_by(category_id=category_id).all()
    return jsonify([{
        "id": a.id,
        "name": a.name,
        "data_type": a.data_type,
        "options": a.options or ""
    } for a in attrs])


# ----------------------
# INIT
# ----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
