from .mock import MockPaymentService

from .stripe import StripeService

from .payment_service import PaymentServiceType


class PaymentServiceFactory:
    mock = False

    @classmethod
    def get_service(cls, payment_service_type):
        if cls.mock:
            return MockPaymentService
        if payment_service_type == PaymentServiceType.STRIPE_SERVICE:
            return StripeService
