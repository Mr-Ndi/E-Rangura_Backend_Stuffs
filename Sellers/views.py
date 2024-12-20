import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Seller

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_seller(request):
    if request.method =='POST':
        try:
            data = json.loads(request.body)
            seller=Seller(
                names=data.get('names'),
                email=data.get('email'),
                password=data.get('password'),
                district=data.get('district'),
                sector=data.get('sector'),
                telephone=data.get('telephone'),
                username=data.get('username'),
                profile_picture=data.get('profile_picture')
            )
            seller.save()
            return JsonResponse({'message':'The seller was created successfully !'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid JSON datum'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)