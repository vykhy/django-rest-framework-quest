from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = serializer.validated_data.get('title')
        serializer.save(content=content)
        # or send a Django signal

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
    
class ProductListAPIView(generics.ListAPIView):
    '''
    Not going to implement this view because ListCreate
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Alternate function based view
@api_view(['GET','POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 
    if method == 'GET':
        if pk is not None:
          obj = get_object_or_404(Product, pk=pk)
          data = ProductSerializer(obj, many=False).data
          return Response(data)
          
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    elif method == 'POST':
        serialized = ProductSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            # instance = serialized.save()
            # instance = form.save()
            content = serialized.validated_data.get('content') or None
            if content is None:
                content = serialized.validated_data.get('title')
            serialized.save(content=content)
            return Response(serialized.data)
        return Response({'invalid': "not good data"}, status=400)
