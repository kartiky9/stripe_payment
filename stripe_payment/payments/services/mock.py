from .payment_service import PaymentService


class MockPaymentService(PaymentService):
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
        return MockPaymentService.get_data()[0]

    @staticmethod
    def list_charges() -> list[dict]:
        return {
            'data': MockPaymentService.get_data()
        }

    @staticmethod
    def create_token(card_number: str, exp_month: int, exp_year: int, cvc: str) -> str:
        if card_number.endswith('4242'):
            return "tk_token"
        else:
            raise Exception("Mock Exception")

    @staticmethod
    def capture_charge(charge_id: str):
        for charge in MockPaymentService.get_data():
            if charge['id'] == charge_id:
                charge['amount_captured'] = charge['amount']
                return charge
        raise Exception("Mock Exception")

    @staticmethod
    def create_refund(charge_id: str):
        for charge in MockPaymentService.get_data():
            if charge['id'] == charge_id:
                charge['amount_refunded'] = charge['amount_captured']
                return charge
        raise Exception("Mock Exception")
