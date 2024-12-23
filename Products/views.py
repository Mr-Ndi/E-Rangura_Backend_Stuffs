from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_product(request):
    if request.method == 'POST':
        try:
            required_fields = ['name', 'price', 'stock_quantity', 'unit', 'minimum_for_deliver', 'description']
            for field in required_fields:
                if field not in request.data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)
            data = request.data

            product = Product(
                name=data.get('name'),
                price=data.get('price'),
                stock_quantity=data.get('stock_quantity'),
                unit=data.get('unit'),
                minimum_for_deliver=data.get('minimum_for_deliver'),
                description=data.get('description'),
                owner_id=request.user
            )
            product.save()
            
            return JsonResponse({'message': 'Product uploaded successfully !','product_id':product.product_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error':'Invalid request method'}, status=405)

@api_view(['GET'])
@permission_classes([AllowAny])
def retrieve_product(request):
    try:
        # Get query parameters
        # product_id = request.GET.get('product_id')
        # owner_id = request.GET.get('owner_id')
        # name = request.GET.get('name')

        # Start with all products
        products = Product.objects.all()

        # Apply filters if parameters are provided
        # if product_id:
        #     products = products.filter(product_id=product_id)
        # if owner_id:
        #     products = products.filter(owner_id=owner_id)
        # if name:
        #     products = products.filter(name__icontains=name)

        # Prepare the response data
        products_data = []
        for product in products:
            products_data.append({
                'product_id': product.product_id,
                'name': product.name,
                'price': product.price,
                'stock_quantity': product.stock_quantity,
                'unit': product.unit,
                'minimum_for_deliver': product.minimum_for_deliver,
                'description': product.description,
                'owner_id': product.owner_id.id if product.owner_id else None,
                'created_at': product.created_at if hasattr(product, 'created_at') else None
            })

        return JsonResponse({
            'message': 'Products retrieved successfully',
            'products': products_data
        }, status=200)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Logging error kugira debugging ishoboke
        return JsonResponse({'error': str(e)}, status=400)