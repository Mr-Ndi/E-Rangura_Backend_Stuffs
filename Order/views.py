from .models import Order
from Products.models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        try:
            required_fields = ['product_id', 'quantity']
            for field in required_fields:
                if field not in request.data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')

            # Fetch the product to ensure it exists and check stock
            try:
                product = Product.objects.get(product_id=product_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

            if quantity > product.stock_quantity:
                return JsonResponse({'error': 'Order quantity exceeds available stock'}, status=400)

            # Create the order
            order = Order(
                owner_id=request.user,
                product_id=product,
                quantity=quantity,
                total_price=quantity * product.price  # Calculate total price
            )
            order.save()

            return JsonResponse({'message': 'Order created successfully!', 'order_id': order.order_id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_user_orders(request):
    try:
        orders = Order.objects.filter(owner_id=request.user)

        # Prepare the response data
        orders_data = []
        for order in orders:
            orders_data.append({
                'order_id': order.order_id,
                'product_id': order.product_id.product_id,
                'quantity': order.quantity,
                'total_price': str(order.total_price),
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat()
            })

        return JsonResponse({
            'message': 'Orders retrieved successfully',
            'orders': orders_data
        }, status=200)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Logging error for debugging
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_user_orders(request):
    try:
        orders = Order.objects.filter(owner_id=request.user)
        
        # Filter by status if provided
        status = request.GET.get('status')
        if status:
            orders = orders.filter(status=status)

        # Prepare the response data
        orders_data = []
        for order in orders:
            orders_data.append({
                'order_id': order.order_id,
                'product_id': order.product_id.product_id,
                'quantity': order.quantity,
                'total_price': str(order.total_price),
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat()
            })

        return JsonResponse({
            'message': 'Filtered orders retrieved successfully',
            'orders': orders_data
        }, status=200)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Logging error for debugging
        return JsonResponse({'error': str(e)}, status=400)
