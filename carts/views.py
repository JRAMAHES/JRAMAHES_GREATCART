from django.shortcuts import render
from django.shortcuts import get_object_or_404
from product.models import Product
from carts.models import Cart, CartItem
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from store.models import Variation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.http import JsonResponse

def _cart_id(request):
    """Generate a unique cart ID for the session."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() # Create a new session if  doesn't exist              
    return cart

def add_cart(request, product_id):
    """Add a product to the cart And redirect to the cart page."""
    # if the user is authenticated, handle the authenticated user case
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)

        variation_product_list = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    variation_product_list.append(variation)  # Add the variation to the list
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=request.user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=request.user)
            existing_variations_list = []
            ids = []
            for item in cart_item:
                existing_variations = item.variation.all()
                existing_variations_list.append(list(existing_variations))
                ids.append(item.id)

            if variation_product_list in existing_variations_list:
                # Increase the cart item quantity
                index = existing_variations_list.index(variation_product_list)
                item_id = ids[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # Create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=request.user)

                if len(variation_product_list) > 0:
                    item.variation.clear() # Clear existing variations
                    item.variation.add(*variation_product_list)
                item.save()  # Save the cart item

        else:
            # Create a new cart item
            cart_item = CartItem.objects.create(product=product, quantity=1, user=request.user)

            if len(variation_product_list) > 0:
                cart_item.variation.clear() # Clear existing variations
                cart_item.variation.add(*variation_product_list)
            cart_item.save()  # Save the cart item
        return redirect('cart')

    # If the user is not authenticated, handle the anonymous user case
    product = Product.objects.get(id=product_id) # get the product by ID

    variation_product_list = []
    if request.method == "POST":
        for item in request.POST:  # Loop through all POST data
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                variation_product_list.append(variation) # Add the variation to the list
            except: 
                pass
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart by session ID 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()  # Save the cart instance

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists: 
        cart_item = CartItem.objects.filter(product=product,cart=cart)

        existing_variations_list = []
        ids = []
        for item in cart_item:
            existing_variations = item.variation.all()
            existing_variations_list.append(list(existing_variations))
            ids.append(item.id)

        if variation_product_list in existing_variations_list:
            index = existing_variations_list.index(variation_product_list)
            item = CartItem.objects.get(product=product, id=ids[index])
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)

            if len(variation_product_list) > 0:
                item.variation.clear() # Clear existing variations
                item.variation.add(*variation_product_list)

            # cart_item.quantity += 1
            item.save()

    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

        if len(variation_product_list) > 0:
            cart_item.variation.clear()  # Clear existing variations
            cart_item.variation.add(*variation_product_list)

        cart_item.save() # Save the cart item

    return redirect('cart')


# ******************** REMOVE CART ITEM FUNCTION ***********************
def remove_cart(request, product_id, cart_item_id):
    """Remove a product from the cart."""
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID(id=product_id)  # Get the product by ID

    try:
        # If the user is authenticated, get the cart item for the user
        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            except CartItem.DoesNotExist:
                return redirect('cart')
        else:
            # If the user is not authenticated, get the cart item for the session
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart by session ID
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is 1
    except CartItem.DoesNotExist:
        pass  # If the item does not exist, do nothing

    return redirect('cart')
# ******************** END OF REMOVE ALL CART ITEMS ***********************

# ******************** REMOVE ALL ITERMS FROM CART ***********************
def remove_cart_item(request, product_id, cart_item_id):
    """Remove all instances of a product from the cart."""
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID    

    if request.user.is_authenticated:
        # If the user is authenticated, get the cart item for the user
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        # If the user is not authenticated, get the cart item for the session
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart by session ID
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    messages.success(request, "Product removed from the cart.")
    return redirect('cart')
# ******************** END OF REMOVE ALL ITERMS FROM CART ***********************

def cart(request, total=0, quantity=0, cart_items=None):
    """Render the cart page. for now, it does not handle any cart logic."""
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * int(0.08))  # Assuming a tax rate of 8%
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,   
    }

    return render(request, 'carts/cart.html', context=context)


# ***************** checkout page functionality *****************
# This view handles the checkout process, calculating totals and rendering the checkout page.
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * int(0.08))  # Assuming a tax rate of 8%
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,   
    }

    return render(request, 'carts/checkout.html', context=context)  
# ***************** END OF checkout page functionality *****************
