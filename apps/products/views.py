from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q, Avg
from .models import Product, Category, Cart, Order, OrderItem, Review, Wishlist, RecentlyViewed
from apps.core.models import Company
from apps.core.utils.email_utils import send_order_confirmation_email
import uuid

def track_recently_viewed(request, product_id):
    """Track product views"""
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id=product_id)
            product.view_count += 1
            product.save()
            
            recently_viewed, created = RecentlyViewed.objects.get_or_create(
                user=request.user,
                product=product
            )
            if not created:
                recently_viewed.save()
            
            recent_items = RecentlyViewed.objects.filter(user=request.user)
            if recent_items.count() > 20:
                for item in recent_items[20:]:
                    item.delete()
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'ok'})

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
    
    if request.user.is_authenticated:
        track_recently_viewed(request, product.id)
    
    related_products = Product.objects.filter(
        category=product.category, 
        status='published'
    ).exclude(id=product.id)[:6]
    
    if related_products.count() < 4:
        featured_products = Product.objects.filter(
            is_featured=True, 
            status='published'
        ).exclude(id=product.id)[:4]
        related_products = list(related_products) + list(featured_products)
    
    seen = set()
    related_products = [p for p in related_products if not (p.id in seen or seen.add(p.id))][:6]
    
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
        
        send_order_confirmation_email(order, request.user)
        
        messages.success(request, f'Order #{order_number} placed successfully! Check your email for confirmation.')
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

@login_required(login_url='/login/')
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')
        
        if rating < 1 or rating > 5:
            messages.error(request, 'Please select a valid rating.')
            return redirect('product_detail', slug=product.slug)
        
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        if existing_review:
            messages.error(request, 'You have already reviewed this product.')
            return redirect('product_detail', slug=product.slug)
        
        has_purchased = Order.objects.filter(
            user=request.user,
            items__product=product,
            status='delivered'
        ).exists()
        
        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            title=title,
            comment=comment,
            is_verified_purchase=has_purchased
        )
        
        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)

@login_required(login_url='/login/')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', review.rating))
        title = request.POST.get('title', review.title)
        comment = request.POST.get('comment', review.comment)
        
        review.rating = rating
        review.title = title
        review.comment = comment
        review.save()
        
        messages.success(request, 'Review updated successfully!')
        return redirect('product_detail', slug=review.product.slug)
    
    context = {'review': review}
    return render(request, 'products/edit_review.html', context)

@login_required(login_url='/login/')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('product_detail', slug=product_slug)

def get_product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product, is_approved=True)
    
    data = {
        'reviews': [
            {
                'user': r.user.username,
                'rating': r.rating,
                'title': r.title,
                'comment': r.comment,
                'created_at': r.created_at.strftime('%B %d, %Y'),
                'is_verified': r.is_verified_purchase
            } for r in reviews
        ],
        'average_rating': product.get_average_rating(),
        'total_reviews': product.get_rating_count()
    }
    return JsonResponse(data)

@login_required(login_url='/login/')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'"{product.name}" added to wishlist! ❤️')
    else:
        messages.info(request, f'"{product.name}" is already in your wishlist.')
    
    return redirect('product_detail', slug=product.slug)

@login_required(login_url='/login/')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'"{product.name}" removed from wishlist.')
    return redirect('wishlist')

@login_required(login_url='/login/')
@require_GET
def wishlist_count(request):
    """API endpoint to get wishlist count for the current user"""
    count = Wishlist.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})

@login_required(login_url='/login/')
def order_detail(request, order_id):
    """View detailed order information with tracking"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    status_order = ['pending', 'processing', 'shipped', 'in_transit', 'out_for_delivery', 'delivered']
    current_index = status_order.index(order.status) if order.status in status_order else 0
    total_steps = len(status_order)
    progress = int((current_index / (total_steps - 1)) * 100) if total_steps > 1 else 0
    
    context = {
        'order': order,
        'progress': progress,
        'status_order': status_order,
        'current_index': current_index,
    }
    return render(request, 'products/order_detail.html', context)

@login_required(login_url='/login/')
def track_order(request):
    """Track order by order number"""
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip().upper()
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            return redirect('order_detail', order_id=order.id)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Please check your order number.')
    
    return render(request, 'products/track_order.html')

@login_required(login_url='/login/')
def update_order_status(request, order_id):
    """Admin only - Update order status"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('order_detail', order_id=order_id)
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
    
    return redirect('order_detail', order_id=order_id)

@login_required(login_url='/login/')
def recently_viewed(request):
    """Show recently viewed products"""
    recent_items = RecentlyViewed.objects.filter(user=request.user).select_related('product')[:20]
    return render(request, 'products/recently_viewed.html', {'recent_items': recent_items})

def search_autocomplete(request):
    """API endpoint for live search suggestions"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query and len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query),
            status='published',
            is_active=True
        )[:10]
        
        categories = Category.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        for product in products:
            results.append({
                'type': 'product',
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'image': product.image.url if product.image else None,
                'url': f'/products/{product.slug}/',
                'category': product.category.name if product.category else 'Uncategorized'
            })
        
        for category in categories:
            results.append({
                'type': 'category',
                'id': category.id,
                'name': category.name,
                'icon': category.icon,
                'url': f'/products/?category={category.slug}'
            })
    
    return JsonResponse({'results': results, 'query': query})
# Update add_to_cart function - remove @login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # If user is not logged in, redirect to login with next parameter
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to add items to your cart.')
        return redirect(f'/login/?next={request.path}')
    
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
# Update add_to_cart function in apps/products/views.py
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # If user is not logged in, redirect to login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to add items to your cart.')
        return redirect(f'/login/?next={request.path}')
    
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
