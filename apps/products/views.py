# Update product_list function in apps/products/views.py
# Remove @login_required decorator - it should be public

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
# Update product_detail function - remove @login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='published')
    
    if request.user.is_authenticated:
        track_recently_viewed(request, product.id)
    
    # Get related products
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
