from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


from .serializers import RequestSerializer
from .services.stripe import StripeServiceFactory


@api_view(['POST'])
def create_charge(request):
    serializer = RequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    StripeService = StripeServiceFactory.get_service()
    try:
        token_id = StripeService.create_token(
            serializer.data['card_number'],
            serializer.data['card_exp_month'],
            serializer.data['card_exp_year'],
            serializer.data['card_cvc']
        )
        charge = StripeService.create_charge(
            token_id,
            serializer.data['amount'],
            serializer.data['currency'],
            serializer.data['description']
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(charge, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def capture_charge(request, chargeId):
    StripeService = StripeServiceFactory.get_service()
    try:
        charge = StripeService.capture_charge(chargeId)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(charge)


@api_view(['POST'])
def create_refund(request, chargeId):
    StripeService = StripeServiceFactory.get_service()
    try:
        refund = StripeService.create_refund(chargeId)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(refund, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_charges(request):
    StripeService = StripeServiceFactory.get_service()
    try:
        charges = StripeService.list_charges()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(charges)
