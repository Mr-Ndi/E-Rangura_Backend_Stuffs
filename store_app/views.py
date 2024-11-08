from django.urls import path
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Product
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Upload product view with improved error handling
@csrf_exempt
def upload_product(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract necessary fields from the data
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            stock_quantity = data.get('stock_quantity')

            # Check if all required fields are provided
            if not name or not description or price is None or stock_quantity is None:
                logger.warning("Missing required fields in product upload request.")
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Create a new product in the database
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity
            )

            # Return success response
            return JsonResponse({'id': product.id, 'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            # Log the error
            logger.error(f"Error creating product: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST, return method not allowed
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# List all products view
def product_list(request):
    if request.method == 'GET':
        try:
            # Retrieve all products from the database
            products = Product.objects.all().values('id', 'name', 'description', 'price', 'stock_quantity')
            return JsonResponse(list(products), safe=False)
        except Exception as e:
            logger.error(f"Error fetching product list: {str(e)}")
            return JsonResponse({'error': 'Failed to fetch products'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Get a single product's details by ID
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            # Retrieve the product by ID, or return 404 if not found
            product = get_object_or_404(Product, id=product_id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),  # Ensure price is returned as a string for JSON response
                'stock_quantity': product.stock_quantity,
            }
            return JsonResponse(product_data)
        except Exception as e:
            logger.error(f"Error fetching product with ID {product_id}: {str(e)}")
            return JsonResponse({'error': 'Product not found or other error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# URL routing for product-related endpoints
urlpatterns = [
    path('upload/', upload_product, name='upload_product'),  # URL to upload a product
    path('products/', product_list, name='product_list'),    # URL to list all products
    path('products/<int:product_id>/', product_detail, name='product_detail'),  # URL to view a single product by ID
]
