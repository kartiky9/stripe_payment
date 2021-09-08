from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.urls import resolve

from .services import MockPaymentService, PaymentServiceFactory

# Create your tests here.


class ChargesTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = [
            {
                'id': 'ch_chargeid_1',
                'amount': 1000,
                'currency': 'inr',
                'amount_captured': 0,
                'amount_refunded': 0,
            },
            {
                'id': 'ch_chargeid_2',
                'amount': 1000,
                'currency': 'inr',
                'amount_captured': 1000,
                'amount_refunded': 0,
            },
            {
                'id': 'ch_chargeid_3',
                'amount': 1000,
                'currency': 'inr',
                'amount_captured': 0,
                'amount_refunded': 1000,
            },
            {
                'id': 'ch_chargeid_4',
                'amount': 1000,
                'currency': 'inr',
                'amount_captured': 500,
                'amount_refunded': 0,
            }
        ]
        MockPaymentService.set_data(cls.data)

    def setUp(self):
        PaymentServiceFactory.mock = True

    def test_create_charge_success(self):
        url = reverse('payments:create-charge')
        data = {
            "amount": 10000,
            "currency": "INR",
            "description": "First Payment",
            "card_number": "4242424242424242",
            "card_exp_month": 1,
            "card_exp_year": 2025,
            "card_cvc": "100"
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_charge_field_missing(self):
        url = reverse('payments:create-charge')
        data = {
            "amount": 10000,
            "description": "First Payment",
            "card_number": "4242424242424242",
            "card_exp_month": 1,
            "card_exp_year": 2025,
            "card_cvc": "100"
        }
        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'currency',
                            status_code=status.HTTP_400_BAD_REQUEST)

    def test_capture_charge_success(self):
        url = reverse('payments:capture-charge', args=['ch_chargeid_1'])

        response = self.client.post(url)
        amount_captured = response.json()['amount_captured']

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'amount_captured')
        self.assertEquals(amount_captured, 1000)

    def test_capture_charge_invalid_chargeId(self):
        url = reverse('payments:capture-charge', args=['some_charge_id'])
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_refund_success(self):
        url = reverse('payments:create-refund', args=['ch_chargeid_4'])

        response = self.client.post(url)
        amount_refunded = response.json()['amount_refunded']

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, 'amount_refunded',
                            status_code=status.HTTP_201_CREATED)
        self.assertEquals(amount_refunded, 500)

    def test_create_refund_invalid_chargeId(self):
        url = reverse('payments:create-refund', args=['some_charge_id'])
        response = self.client.post(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_charges_success(self):
        url = reverse('payments:get-charges')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(self.__class__.data, response.json()['data'])
