from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ProductImage, Cart, CartItem, Product, Wishlist, Order, OrderItem, Address
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def product_list(request):
    # Get all products or filter by category if specified
    category_id = request.GET.get('category')
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 5)  # 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    context = {
        'product': product,
        'images': images,
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart-detail')

@login_required
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
    return redirect('cart-detail')

@login_required
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart-detail')


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist-list')

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product__id=product_id).delete()
    return redirect('wishlist-list')

@login_required
def wishlist_list(request):
    wishlisted_products = Product.objects.filter(wishlisted_by__user=request.user)
    return render(request, 'store/wishlist.html', {'wishlisted_products': wishlisted_products})


@login_required
def checkout(request):
    addresses = Address.objects.filter(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            status='Pending'
        )

        # Move cart items to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Clear cart
        cart.items.all().delete()
        return redirect('order-success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
    })

def order_success(request):
    return render(request, 'store/order_success.html')
