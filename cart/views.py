from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product  
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()  # Corrected function call
    quantities = cart.get_quants()  #  Get the quantity mapping
    total = cart.cart_total()  # Get the cart total
    return render(request, "cart_summary.html", {
        "cart_products": cart_products,
        "quantities": quantities,  #  Pass quantities to template
        "totals": total            # Pass total to template
    })

def cart_update(request):
    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.update(product, product_qty)  # Updates the cart

        response = JsonResponse({'success': True})
        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)  # Fetch the product object
        cart.delete(product)  # Pass the product object to delete from cart
        response = JsonResponse({'product': product_id})
        return response

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))  # Convert to string for dictionary keys
        product_qty = int(request.POST.get('product_qty'))  # Get the quantity from the AJAX request

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)  # Pass quantity to the cart

        cart_quantity = cart.__len__()  # Get updated cart quantity

        response = JsonResponse({'qty': cart_quantity})
        return response
