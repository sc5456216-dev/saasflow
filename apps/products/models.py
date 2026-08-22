from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Company

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('out_of_stock', 'Out of Stock'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    images = models.JSONField(default=list, blank=True)
    
    stock = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    def is_in_stock(self):
        return self.stock > 0
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / reviews.count()
        return 0
    
    def get_rating_count(self):
        return self.reviews.count()
    
    def is_in_wishlist(self, user):
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user, product=self).exists()
        return False
    
    class Meta:
        ordering = ['-created_at']

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.viewed_at}"
    
    class Meta:
        ordering = ['-viewed_at']
        unique_together = ['user', 'product']

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}⭐"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        unique_together = ['user', 'product']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    
    order_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    billing_address = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, default='pending')
    
    tracking_number = models.CharField(max_length=100, blank=True)
    tracking_url = models.URLField(blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    def get_status_icon(self):
        icons = {
            'pending': '⏳',
            'processing': '🔄',
            'shipped': '📦',
            'in_transit': '🚚',
            'out_for_delivery': '🚛',
            'delivered': '✅',
            'cancelled': '❌',
        }
        return icons.get(self.status, '📦')
    
    def get_status_color(self):
        colors = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'processing': 'bg-blue-100 text-blue-800',
            'shipped': 'bg-purple-100 text-purple-800',
            'in_transit': 'bg-indigo-100 text-indigo-800',
            'out_for_delivery': 'bg-orange-100 text-orange-800',
            'delivered': 'bg-green-100 text-green-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return colors.get(self.status, 'bg-gray-100 text-gray-800')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
# Add to apps/products/models.py in Product class

def get_stock_status(self):
    """Get stock status with thresholds"""
    if self.stock <= 0:
        return {'status': 'out_of_stock', 'label': 'Out of Stock', 'color': 'red', 'icon': '❌'}
    elif self.stock <= 5:
        return {'status': 'low_stock', 'label': 'Low Stock', 'color': 'orange', 'icon': '⚠️'}
    elif self.stock <= 20:
        return {'status': 'limited', 'label': 'Limited Stock', 'color': 'yellow', 'icon': '🟡'}
    else:
        return {'status': 'in_stock', 'label': 'In Stock', 'color': 'green', 'icon': '✅'}

def get_stock_badge_html(self):
    """Get HTML for stock badge"""
    status = self.get_stock_status()
    colors = {
        'green': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'orange': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        'yellow': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        'red': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    }
    return f'<span class="px-3 py-1 rounded-full text-sm font-medium {colors.get(status["color"], colors["green"])}">{status["icon"]} {status["label"]}</span>'

def is_low_stock(self):
    """Check if product is low on stock"""
    return self.stock > 0 and self.stock <= 5
