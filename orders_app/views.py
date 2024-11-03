from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).values(
            'id', 'order_date', 'total_amount', 'status'
        )
        return JsonResponse(list(orders), safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user == request.user:
        order_data = {
            'id': order.id,
            'order_date': order.order_date,
            'total_amount': order.total_amount,
            'status': order.status,
            'items': list(order.orderitem_set.values(
                'product__name', 'quantity', 'price_at_purchase'
            ))
        }
        return JsonResponse(order_data)
    else:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
