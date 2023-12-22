from django.forms.models import model_to_dict
from django.http import JsonResponse
from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().first()
    return JsonResponse(model_to_dict(model_data))
