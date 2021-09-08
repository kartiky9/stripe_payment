from abc import ABCMeta, abstractstaticmethod
from enum import Enum, auto


class PaymentServiceType(Enum):
    STRIPE_SERVICE = auto()


class PaymentService(metaclass=ABCMeta):
    @abstractstaticmethod
    def create_charge(token_id: str, amount: int, currency: str, description: str) -> dict:
        pass

    @abstractstaticmethod
    def list_charges() -> list[dict]:
        pass

    @abstractstaticmethod
    def create_token(card_number: str, exp_month: int, exp_year: int, cvc: str) -> str:
        pass

    @abstractstaticmethod
    def capture_charge(charge_id: str):
        pass

    @abstractstaticmethod
    def create_refund(charge_id: str):
        pass
