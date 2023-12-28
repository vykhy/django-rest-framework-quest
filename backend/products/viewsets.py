from rest_framework import viewsets, mixins

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> List -> Queryset
    get -> Retrieve -> Product Instance Details
    post -> Create -> Create New Instance
    put -> Update
    patch -> Partial Update
    delete -> Destroy
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Generic Viewsets
class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'