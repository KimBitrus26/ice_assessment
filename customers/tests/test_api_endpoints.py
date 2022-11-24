from datetime import datetime
import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from customers.models import Customer, Payment
from customers.utils import Helper


class IsNotStaffTesting(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="john@gmailcom",
            password="johnpassword123",
            full_name="John Doe",
            is_staff=False
        )
        self.client.force_authenticate(self.user)

    def test_user_not_is_staff_not_allowed_api(self):
        """Test is not is not staff cannot create customer"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }

        res = self.client.post("/api/v1/customer/", payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class APIStaffTesting(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="john@gmailcom",
            password="johnpassword123",
            full_name="John Doe",
            is_staff=True
        )
        self.client.force_authenticate(self.user)


    def test_create_customer_api(self):
        """Test to create customer api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }

        res = self.client.post("/api/v1/customer/", payload)
        customer = Customer.objects.get(id=res.data['data']['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(customer.id, res.data['data']['id'])
        self.assertEqual(customer.name, res.data['data']['name'])
        self.assertEqual(customer.address, res.data['data']['address'])
        self.assertEqual(customer.phone_number, res.data['data']['phone_number'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(customer, key))

    def test_retrieve_single_customer_api(self):
        """Test to retrieve a single customer api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)
        # retrieve customer
        res2 = self.client.get(f"/api/v1/customer/{res.data['data']['slug']}/")
        # import pdb
        # pdb.set_trace()
        customer = Customer.objects.get(id=res2.data['data']['id'])

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(customer.id, res2.data['data']['id'])
        self.assertEqual(customer.name, res2.data['data']['name'])
        self.assertEqual(customer.address, res2.data['data']['address'])
        self.assertEqual(customer.phone_number, res2.data['data']['phone_number'])

    def test_update_single_customer_api(self):
        """Test to update a single customer api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)
        # update customer
        payload2 = {
            "name": "kevin hart",
            "address": "jos",
        }
        res2 = self.client.patch(f"/api/v1/customer/{res.data['data']['slug']}/", payload2)

        customer = Customer.objects.get(id=res2.data['data']['id'])

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(customer.id, res2.data['data']['id'])
        self.assertEqual(customer.name, payload2['name'])
        self.assertEqual(customer.address, payload2['address'])
        self.assertEqual(customer.phone_number, res2.data['data']['phone_number'])

    def test_delete_single_customer_api(self):
        """Test to delete a single customer api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)
        # delete customer
        res2 = self.client.delete(f"/api/v1/customer/{res.data['data']['slug']}/")
        self.assertEqual(res2.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_customers_api(self):
        """Test to get all customers api"""

        Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )
        Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )

        # get all customer
        res = self.client.get(f"/api/v1/customer/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 2)

    def test_create_customer_payment_api(self):
        """Test to create customer payment api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)

        # create customer payment
        payload2 = {
            "amount": 302,
            "verified": True
        }
        res2 = self.client.post(f"/api/v1/customer-payment/{res.data['data']['slug']}/", payload2)

        payment = Payment.objects.get(id=res2.data['data']['id'])

        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payment.id, res2.data['data']['id'])
        self.assertEqual(payment.amount, payload2['amount'])
        self.assertEqual(payment.verified, payload2['verified'])

    def test_get_single_customer_payment_api(self):
        """Test to get a single customer payment api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)

        # create customer payment
        payload2 = {
            "amount": 302,
            "verified": True
        }
        res2 = self.client.post(f"/api/v1/customer-payment/{res.data['data']['slug']}/", payload2)

        # get single customer payment
        res3 = self.client.get(f"/api/v1/customer-payment-detail/{res2.data['data']['slug']}/")
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 1)

    def test_get_all_customer_payment_api(self):
        """Test to get all  payment of a particular customer api"""

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)

        # create customer payments
        payload2 = {
            "amount": 302,
            "verified": True
        }
        self.client.post(f"/api/v1/customer-payment/{res.data['data']['slug']}/", payload2)
        import time
        time.sleep(3)  # create another instance of customer payment
        self.client.post(f"/api/v1/customer-payment/{res.data['data']['slug']}/", payload2)

        # get all payments of a particular customer
        res3 = self.client.get(f"/api/v1/customer-payment-multiple/{res.data['data']['slug']}/")
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 2)

    def test_get_all_payments_api(self):
        """Test to get all  payments api"""

        customer = Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )
        Payment.objects.create(
            amount=301,
            verified=True,
            customer=customer,
            reference="rehdghff65fhth"
        )

        payload = {
            "name": "john doe",
            "address": "abuja",
            "phone_number": "09098765432",
            "email": "email@gmail.com"
        }
        # create the customer
        res = self.client.post("/api/v1/customer/", payload)
        # create customer payments
        payload2 = {
            "amount": 302,
            "verified": True
        }
        self.client.post(f"/api/v1/customer-payment/{res.data['data']['slug']}/", payload2)

        # get all payments
        res3 = self.client.get(f"/api/v1/customer-payments/")
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 2)

    def test_saerch_customer_api(self):
        """Test to search customer"""

        Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="john@gmail.com",
            phone_number="08098654323"
        )
        Customer.objects.create(
            name="John Doe",
            address="Abuja",
            email="new@gmail.com",
            phone_number="08098654323"
        )
        search_word = "new@gmail.com"
        search_res = self.client.get(f"/api/v1/search?query={search_word}")
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
