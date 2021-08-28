from rest_framework import serializers

from .utils import get_current_year, get_current_month


class RequestSerializer(serializers.Serializer):
    """
    Request Serializer as per required by Stripe API. Validations used are as per required for Stripe API
    """

    amount = serializers.IntegerField(min_value=50, max_value=99999999)
    currency = serializers.CharField(max_length=3)
    description = serializers.CharField(
        max_length=200, required=False, allow_null=True)
    card_number = serializers.CharField(
        min_length=16, max_length=16, required=False)
    card_exp_month = serializers.IntegerField(
        min_value=1, max_value=12, required=False)
    card_exp_year = serializers.IntegerField(min_value=2000, required=False)
    card_cvc = serializers.CharField(
        min_length=3, max_length=3, required=False)

    def validate(self, attrs):
        """
        Check if Card Expiry month and year are not past
        """
        if attrs['card_exp_year'] < get_current_year():
            raise serializers.ValidationError(
                'card_exp_year cannot be from past')
        if attrs['card_exp_year'] == get_current_year() and attrs['card_exp_month'] < get_current_month():
            raise serializers.ValidationError(
                'card_exp_month cannot be from past'
            )
        return attrs
