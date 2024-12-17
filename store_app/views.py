from django.urls import path
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Product
import logging
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_product(request):
    logger.info("Received request method: %s", request.method)
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

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
                stock_quantity=stock_quantity,
                owner=request.user
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

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product = get_object_or_404(Product, id=product_id)

        
            if product.owner != request.user:
                return JsonResponse({'error': 'You do not have permission to update this product.'}, status=403)

            name = data.get('name', product.name) 
            description = data.get('description', product.description)
            price = data.get('price', product.price)
            stock_quantity = data.get('stock_quantity', product.stock_quantity)

        
            if name:
                product.name = name
            if description:
                product.description = description
            if price is not None:
                product.price = price
            if stock_quantity is not None:
                product.stock_quantity = stock_quantity

            product.save()

            return JsonResponse({'message': 'Product updated successfully!'}, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            logger.error(f"Error updating product with ID {product_id}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = get_object_or_404(Product, id=product_id)

        
            if product.owner != request.user:
                return JsonResponse({'error': 'You do not have permission to delete this product.'}, status=403)

            product.delete()
            
            return JsonResponse({'message': 'Product deleted successfully!'}, status=204)

        except Exception as e:
            logger.error(f"Error deleting product with ID {product_id}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def my_product_list(request):
    if request.method == 'GET':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

            products = Product.objects.filter(owner=request.user).values('id', 'name', 'description', 'price', 'stock_quantity')
            return JsonResponse(list(products), safe=False)
        except Exception as e:
            logger.error(f"Error fetching user's products: {str(e)}")
            return JsonResponse({'error': 'Failed to fetch products'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


urlpatterns = [
    path('upload/', upload_product, name='upload_product'), 
    path('products/', product_list, name='product_list'),   
    path('products/<int:product_id>/', product_detail, name='product_detail'), 
    path('products/update/<int:product_id>/', update_product, name='update_product'), 
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'), 
    path('my-products/', my_product_list, name='my_product_list'), 
]
