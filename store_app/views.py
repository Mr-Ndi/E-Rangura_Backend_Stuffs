from django.urls import path
import json
from django.http import JsonResponse
from .views import product_list, product_detail
from django.views.decorators.csrf import csrf_exempt
from .models import Product

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
]

@csrf_exempt
def upload_product(request):
    if request.method == 'POST':
        try:
    
            data = json.loads(request.body)

    
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            stock_quantity = data.get('stock_quantity')

    
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity
            )

    
            return JsonResponse({'id': product.id, 'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)