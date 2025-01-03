import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Seller
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
@permission_classes([AllowAny])
def create_seller(request):
    if request.method =='POST':
        try:
            data = json.loads(request.body)
            if Seller.objects.filter(email=data.get('email')).exists():
                return JsonResponse({'error': 'A seller with this email already exists.'}, status=400)

            if Seller.objects.filter(username=data.get('username')).exists():
                return JsonResponse({'error': 'A seller with this username already exists.'}, status=400)
            seller=Seller(
                names=data.get('names'),
                email=data.get('email'),
                password=make_password(data.get('password')),
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


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'message': 'Login succesfull',
            'User': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=200)
    
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token is required'}, status=400)

        RefreshToken(refresh_token).blacklist()

        return JsonResponse({'message': 'Logout successful'}, status=205)  # 205 Reset Content

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)