from django.urls import path
import json
from django.http import JsonResponse
from .views import product_list, product_detail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
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

def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all().values('id', 'name', 'description', 'price', 'stock_quantity')
        return JsonResponse(list(products), safe=False)

def product_detail(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),  
            'stock_quantity': product.stock_quantity,
        }
        return JsonResponse(product_data)
