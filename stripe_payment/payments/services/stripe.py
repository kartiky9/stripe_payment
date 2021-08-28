import functools

import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


class StripeServiceFactory:
    mock = False

    @classmethod
    def get_service(cls):
        if cls.mock:
            return _MockStripeService
        return _StripeService


class _StripeService:
    @staticmethod
    def create_charge(token_id: str, amount: int, currency: str, description: str) -> dict:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            description=description,
            source=token_id,
            capture=False
        )
        return charge

    @staticmethod
    def list_charges() -> list[dict]:
        """ Returns list of charges """
        charges = stripe.Charge.list(limit=100)
        charges.pop('object')
        charges.pop('url')
        return charges

    @staticmethod
    def create_token(card_number: str, exp_month: int, exp_year: int, cvc: str) -> str:
        """Generates token wih card payment required by stripe api to create charge object

        Args:
            card_number (str): Credit Card Number. (Test Card Number - 4242424242424242)
            exp_month (int): Credit Card Expiry Month
            exp_year (int):  Credit Card Expiry Month
            cvc (str):  Card CVC

        Returns:
            str: Token Id generated by stripe
        """
        token = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc
            }
        )

        return token['id']

    @staticmethod
    def capture_charge(charge_id: str):
        return stripe.Charge.capture(
            charge_id
        )

    @staticmethod
    def create_refund(charge_id: str):
        return stripe.Refund.create(
            charge=charge_id
        )


class _MockStripeService:
    mock_data: dict

    @classmethod
    def set_data(cls, data: list):
        cls.mock_data = data

    @classmethod
    def get_data(cls):
        return cls.mock_data

    @staticmethod
    def create_charge(token_id: str, amount: int, currency: str, description: str) -> dict:
        if not token_id.startswith('tk'):
            raise Exception("Mock Exception")
        return _MockStripeService.get_data()[0]

    @staticmethod
    def list_charges() -> list[dict]:
        return {
            'data': _MockStripeService.get_data()
        }

    @staticmethod
    def create_token(card_number: str, exp_month: int, exp_year: int, cvc: str) -> str:
        if card_number.endswith('4242'):
            return "tk_token"
        else:
            raise Exception("Mock Exception")

    @staticmethod
    def capture_charge(charge_id: str):
        for charge in _MockStripeService.get_data():
            if charge['id'] == charge_id:
                charge['amount_captured'] = charge['amount']
                return charge
        raise Exception("Mock Exception")

    @staticmethod
    def create_refund(charge_id: str):
        for charge in _MockStripeService.get_data():
            if charge['id'] == charge_id:
                charge['amount_refunded'] = charge['amount_captured']
                return charge
        raise Exception("Mock Exception")