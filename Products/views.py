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