import unittest
from db import create_app, db
from models import Category, Attribute, Product, ProductAttributeValue

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product_with_attributes(self):
        cat = Category(name="Smartphones")
        attr = Attribute(name="OS", data_type="text", category=cat)
        db.session.add(cat)
        db.session.add(attr)
        db.session.commit()

        p = Product(name="Phone X", sku="PX1", price=499.99, category=cat)
        db.session.add(p)
        db.session.flush()

        val = ProductAttributeValue(product=p, attribute=attr)
        val.set_value("Android")
        db.session.add(val)
        db.session.commit()

        self.assertEqual(p.attribute_values[0].get_value(), "Android")

if __name__ == "__main__":
    unittest.main()
