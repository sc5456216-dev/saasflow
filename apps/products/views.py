from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from .models import Product, Category, Cart, Order, OrderItem
from apps.core.models import Company
import uuid

def product_list(request):
    products = Product.objects.filter(status='published', is_active=True)
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='published')
    related_products = Product.objects.filter(category=product.category, status='published').exclude(id=product.id)[:4]
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Product image updated successfully!')
            return redirect('product_detail', slug=product.slug)
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to cart!',
            'cart_count': Cart.objects.filter(user=request.user).count()
        })
    
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('view_cart')

@login_required(login_url='/login/')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'products/cart.html', context)

@login_required(login_url='/login/')
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')

@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('product_list')
    
    if request.method == 'POST':
        company = Company.objects.filter(owner=request.user).first()
        
        total = sum(item.get_total_price() for item in cart_items)
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            user=request.user,
            company=company,
            order_number=order_number,
            total_amount=total,
            shipping_address=request.POST.get('shipping_address'),
            billing_address=request.POST.get('billing_address', request.POST.get('shipping_address')),
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                subtotal=item.get_total_price()
            )
        
        cart_items.delete()
        
        messages.success(request, f'Order #{order_number} placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    total = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'products/checkout.html', context)

@login_required(login_url='/login/')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_confirmation.html', {'order': order})

@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_history.html', {'orders': orders})

@login_required(login_url='/login/')
@require_GET
def cart_count(request):
    """API endpoint to get cart count for the current user"""
    count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})
