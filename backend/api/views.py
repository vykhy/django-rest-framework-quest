from django.forms.models import model_to_dict

from products.models import Product
from products.serializers import ProductSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().first()
    data = ProductSerializer(instance).data
    return Response(data)


