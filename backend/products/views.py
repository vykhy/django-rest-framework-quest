from rest_framework import generics, mixins, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from api.mixins import (StaffEditorPermissionMixin, UserQuerySetMixin)

class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = serializer.validated_data.get('title')
        serializer.save(content=content, user=self.request.user)
        # or send a Django signal
    
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset()
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)
        

class ProductDetailAPIView(
    UserQuerySetMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
    
class ProductListAPIView(
    UserQuerySetMixin,generics.ListAPIView):
    '''
    Not going to implement this view because ListCreate
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateAPIView(
    UserQuerySetMixin,StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDeleteAPIView(
    UserQuerySetMixin,StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

# Alternate Generic View
class ProductMixinView(
    UserQuerySetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = serializer.validated_data.get('title')
        serializer.save(content=content)
        # or send a Django signal

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
