from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from .validators import validate_title, validate_title_no_hello, unique_product_title

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')

    # email = serializers.EmailField(write_only=True)

    title = serializers.CharField(validators=[validate_title, validate_title_no_hello, unique_product_title])

    # Also supports foreign key relations
    # name = serializers.CharField(source='title', read_only=True)
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
            'edit_url',
            'name'
        ]
    
    def create(self, validated_data):
        # return Product.objects.create(**validated_data) this is the default behaviour
        # email = validated_data.pop('email')
        # We can also do this in the View with serializer.save()
        obj = super().create(validated_data)
        return obj
    
    def update(self, instance, validated_data):
        return instance
    
    # In-line is useful if we need the request context
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     qs = Product.objects.filter(user=request.user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        
        return reverse("product-edit", kwargs={"pk":obj.pk}, request=request)
    
    def get_discount(self, obj):
        if not hasattr(obj, 'id') or not isinstance(obj, Product):
            return None
        return obj.get_discount()