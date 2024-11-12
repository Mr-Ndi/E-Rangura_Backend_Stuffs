from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from store_app.models import Product
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Ensure the user is logged in
            user = request.user

            # Create the order
            order = Order.objects.create(user=user)

            # Add items to the order
            order_items = data.get('items', [])
            total_amount = 0
            for item in order_items:
                product = get_object_or_404(Product, id=item['product_id'])
                quantity = item['quantity']
                price_at_purchase = product.price
                total_amount += price_at_purchase * quantity

                # Create an OrderItem entry for each product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=price_at_purchase,
                )

            # Update total amount on order
            order.total_amount = total_amount
            order.save()

            return JsonResponse({
                'id': order.id,
                'message': 'Order created successfully!',
                'total_amount': total_amount,
                'items': order_items
            }, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

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
