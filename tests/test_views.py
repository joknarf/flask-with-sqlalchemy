# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, db
from models import Product

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_products_get(self):
        response = self.client.get("/products/1")
        product = response.json
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Skello')

    def test_product_404(self):
        response = self.client.get("/products/1000")
        self.assertEqual(response.status_code, 404)

    def test_product_create(self):
        response = self.client.post("/products", json={"name": "Peche.tv"})
        product = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(product['name'], 'Peche.tv')

    def test_product_delete(self):
        response = self.client.delete("/products/3")
        self.assertEqual(response.status_code, 204)

    def test_product_update(self):
        response = self.client.patch("/products/2", json={"name":"yop"})
        product = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(product['name'], 'yop')

    def test_product_update(self):
        response = self.client.patch("/products/2", json={"name":""})
        self.assertEqual(response.status_code, 422)
