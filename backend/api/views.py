from django.forms.models import model_to_dict

from products.models import Product
from products.serializers import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    # instance = Product.objects.all().first()
    # data = ProductSerializer(instance).data

    serialized = ProductSerializer(data=request.data)
    if serialized.is_valid():

        return Response(serialized.data)
    # return Response({"message": "Invalid data"}, status=400)


