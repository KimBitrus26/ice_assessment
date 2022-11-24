from django.test import TestCase

from customers.models import Customer, Payment


class ModelTests(TestCase):

    def test_create_customer_model(self):
        """Test create customer instance"""

        customer = Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )

        self.assertTrue(isinstance(customer, Customer))
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(str(customer), f"{customer.name}")

    def test_create_customer_model(self):
        """Test create payment instance"""

        customer = Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )
        payment = Payment.objects.create(
            amount=301,
            verified=True,
            customer=customer
        )
        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(str(payment), f"{payment.customer.name} payment")
