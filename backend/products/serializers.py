from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')

    # email = serializers.EmailField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'sale_price',
            'discount',
            'url',
            'edit_url'
        ]
    
    def create(self, validated_data):
        # return Product.objects.create(**validated_data) this is the default behaviour
        # email = validated_data.pop('email')
        # We can also do this in the View with serializer.save()
        obj = super().create(validated_data)
        return obj
    
    def update(self, instance, validated_data):
        return instance

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        
        return reverse("product-edit", kwargs={"pk":obj.pk}, request=request)
    
    def get_discount(self, obj):
        if not hasattr(obj, 'id') or not isinstance(obj, Product):
            return None
        return obj.get_discount()