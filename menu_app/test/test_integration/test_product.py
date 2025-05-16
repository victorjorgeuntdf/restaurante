from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from menu_app.models import Product


class BaseProductTestCase(TestCase):
    """Clase base con la configuración común para todos los tests de productos"""

    def setUp(self):
        fake_image = SimpleUploadedFile(
            name="test.jpg", content=b"file_content", content_type="image/jpeg"
        )
        # Crear algunos productos de prueba
        self.product1 = Product.objects.create(
            name="Producto 1",
            description="Descripción del producto 1",
            price=10,
            quantity=15,
            image=fake_image,
        )

        self.product2 = Product.objects.create(
            name="Producto 2",
            description="Descripción del producto 2",
            price=20,
            quantity=1,
            image=fake_image,
        )

        # Cliente para hacer peticiones
        self.client = Client()


class ProductsListViewTest(BaseProductTestCase):
    """Tests para la vista de listado de productos"""

    def test_products_view(self):
        """Test que verifica que la vista products funciona"""
        # Hacer petición a la vista products
        response = self.client.get(reverse("menu"))

        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu_app/menu.html")
        self.assertIn("menu_items", response.context)
        self.assertEqual(len(response.context["menu_items"]), 2)

        # Verificar que los productos están ordenados por fecha
        products = list(response.context["menu_items"])
        self.assertEqual(products[0].id, self.product1.id)
        self.assertEqual(products[1].id, self.product2.id)


class ProductDetailViewTest(BaseProductTestCase):
    """Tests para la vista de detalle de un producto"""

    def test_product_detail_view(self):
        """Test que verifica que la vista product_detail funciona"""

        # Hacer petición a la vista product_detail
        response = self.client.get(reverse("product_detail", args=[self.product1.id]))

        # Verificar respuesta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu_app/product_detail.html")
        self.assertIn("product", response.context)
        self.assertEqual(response.context["product"].id, self.product1.id)
