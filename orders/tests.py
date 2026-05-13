from django.test import TestCase
from rest_framework.test import APIClient

from books.models import Book, Publisher
from cart.models import Cart, CartItem
from users.models import User


class CartClearedAfterOrderTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='buyer@test.com',
            password='testpass123',
            native_name='Buyer',
        )
        publisher = Publisher.objects.create(
            name='Test Publisher',
            description='Test description',
            logo='',
        )
        self.book = Book.objects.create(
            title='Test Book',
            description='Test description',
            price=100,
            cover='',
            publisher=publisher,
            pages=100,
            cover_type='soft',
            language='uk',
            isbn='1234567890001',
            quantity=5,
        )
        self.cart = Cart.objects.create(customer=self.user)
        CartItem.objects.create(cart=self.cart, book=self.book, price=100, quantity=1)

    def test_cart_is_deleted_after_order_created(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/order/create/', {
            'name': 'Test',
            'surname': 'Buyer',
            'delivery_type': 'self',
            'payment_method': 'online',
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertFalse(
            Cart.objects.filter(customer=self.user).exists(),
            'Cart should be deleted after the order is created',
        )
        self.assertEqual(
            CartItem.objects.filter(cart=self.cart).count(),
            0,
            'All cart items should be gone after the order is created',
        )
