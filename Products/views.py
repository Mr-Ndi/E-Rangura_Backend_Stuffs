from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Product(
                name=data.get('name'),
                price=data.get('price'),
                stock_quantity=data.get('stock_quantity'),
                unit=data.get('data'),
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
def retrive_product(request):
    try:
        product_id = request.GET.get('product_id')
        owner_id = request.GET.get('owner_id')
        name = request.Get.get('name')

        products = Product.objects.all()

        if product_id:
            prodocts = Product.filter(product_id=product_id)
        if owner_id:
            prodocts = Product.filter(owner_id=owner_id)
        if name:
            prodocts = Product.filter(name=name)

        products_data = []
        for product in products:
            products_data.append({
                'product_is': product.product_id,
                'name': product.name,
                'price': product.price,
                'stock_quantity': product.stock_quantity,
                'unit': product.unit,
                'minimum_for_deliver': product.minimum_for_deliver,
                'description':product.description,
                'owner_id': product.owner_id,
                # 'created_at': product.created_at if hasattr(product, 'created_at') else None
            })

        return JsonResponse({
            'message': 'Product retrived succesfully',
            'products': products_data},
            stsus=200)
    except Product.DoesNotExist:
        return JsonResponse({
            'error': 'No products found'
        },
        statuscode = 404)
    except Exception as e:
        return JsonResponse({
            'error':str(e)
        },
        status=400
        )