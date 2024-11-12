from django.urls import path
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Product
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def upload_product(request):
    logger.info("Received request method: %s", request.method)
    if request.method == 'POST':
        try:
        
            data = json.loads(request.body)

        
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            stock_quantity = data.get('stock_quantity')

        
            if not name or not description or price is None or stock_quantity is None:
                logger.warning("Missing required fields in product upload request.")
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity
            )

        
            return JsonResponse({'id': product.id, 'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
        
            logger.error(f"Error creating product: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


    return JsonResponse({'error': 'Invalid request method'}, status=405)


def product_list(request):
    if request.method == 'GET':
        try:
        
            products = Product.objects.all().values('id', 'name', 'description', 'price', 'stock_quantity')
            return JsonResponse(list(products), safe=False)
        except Exception as e:
            logger.error(f"Error fetching product list: {str(e)}")
            return JsonResponse({'error': 'Failed to fetch products'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def product_detail(request, product_id):
    if request.method == 'GET':
        try:
        
            product = get_object_or_404(Product, id=product_id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price), 
                'stock_quantity': product.stock_quantity,
            }
            return JsonResponse(product_data)
        except Exception as e:
            logger.error(f"Error fetching product with ID {product_id}: {str(e)}")
            return JsonResponse({'error': 'Product not found or other error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


urlpatterns = [
    path('upload/', upload_product, name='upload_product'), 
    path('products/', product_list, name='product_list'),   
    path('products/<int:product_id>/', product_detail, name='product_detail'), 
]
