import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, Category
from django.contrib.auth.models import User

def add_products():
    # Create categories
    categories_data = [
        {'name': 'Software', 'slug': 'software'},
        {'name': 'Services', 'slug': 'services'},
        {'name': 'Templates', 'slug': 'templates'},
        {'name': 'Courses', 'slug': 'courses'},
        {'name': 'Tools', 'slug': 'tools'},
    ]
    
    categories = []
    for cat in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat['slug'],
            defaults={'name': cat['name']}
        )
        categories.append(category)
        if created:
            print(f'✅ Category created: {category.name}')
    
    # Get first user
    user = User.objects.first()
    if not user:
        print('❌ No user found! Create a superuser first.')
        return
    
    # Products with real images
    products_data = [
        {
            'name': 'Premium SaaS Plan',
            'slug': 'premium-saas-plan',
            'description': 'Full access to all premium features including AI, analytics, and unlimited users. Perfect for growing businesses.',
            'short_description': 'Unlock all premium features',
            'price': 99.99,
            'compare_price': 149.99,
            'stock': 100,
            'is_featured': True,
            'status': 'published',
            'is_active': True,
            'category': categories[0]
        },
        {
            'name': 'Pro Plan',
            'slug': 'pro-plan',
            'description': 'Advanced features for power users with priority support and advanced analytics.',
            'short_description': 'Advanced features + priority support',
            'price': 49.99,
            'compare_price': 79.99,
            'stock': 200,
            'is_featured': True,
            'status': 'published',
            'is_active': True,
            'category': categories[0]
        },
        {
            'name': 'Starter Kit',
            'slug': 'starter-kit',
            'description': 'Everything you need to get started with SaaSFlow. Includes basic features and email support.',
            'short_description': 'Complete starter package',
            'price': 29.99,
            'stock': 500,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[0]
        },
        {
            'name': 'Analytics Dashboard Pro',
            'slug': 'analytics-dashboard-pro',
            'description': 'Real-time analytics dashboard with custom reports, user behavior tracking, and business insights.',
            'short_description': 'Real-time analytics dashboard',
            'price': 79.99,
            'compare_price': 129.99,
            'stock': 150,
            'is_featured': True,
            'status': 'published',
            'is_active': True,
            'category': categories[0]
        },
        {
            'name': 'Cloud Storage Pro',
            'slug': 'cloud-storage-pro',
            'description': 'Secure cloud storage with 1TB space, end-to-end encryption, and automatic backup.',
            'short_description': '1TB secure cloud storage',
            'price': 59.99,
            'compare_price': 89.99,
            'stock': 300,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[1]
        },
        {
            'name': 'API Management Suite',
            'slug': 'api-management-suite',
            'description': 'Complete API management with authentication, rate limiting, analytics, and documentation.',
            'short_description': 'Full API management platform',
            'price': 149.99,
            'compare_price': 249.99,
            'stock': 80,
            'is_featured': True,
            'status': 'published',
            'is_active': True,
            'category': categories[4]
        },
        {
            'name': 'Web Development Bootcamp',
            'slug': 'web-dev-bootcamp',
            'description': 'Complete full-stack web development course with 40+ hours of video content and real-world projects.',
            'short_description': 'Full-stack web development course',
            'price': 199.99,
            'compare_price': 299.99,
            'stock': 200,
            'is_featured': True,
            'status': 'published',
            'is_active': True,
            'category': categories[3]
        },
        {
            'name': 'Design System Templates',
            'slug': 'design-system-templates',
            'description': '100+ premium UI components and templates for your next project. Includes Figma files.',
            'short_description': '100+ premium UI templates',
            'price': 39.99,
            'compare_price': 59.99,
            'stock': 150,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[2]
        },
        {
            'name': 'Email Marketing Pro',
            'slug': 'email-marketing-pro',
            'description': 'AI-powered email marketing platform with automation, segmentation, and advanced analytics.',
            'short_description': 'AI email marketing platform',
            'price': 69.99,
            'compare_price': 99.99,
            'stock': 600,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[0]
        },
        {
            'name': 'Security Audit Service',
            'slug': 'security-audit-service',
            'description': 'Professional security audit with vulnerability scanning, penetration testing, and detailed reports.',
            'short_description': 'Professional security audit',
            'price': 299.99,
            'stock': 50,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[1]
        }
    ]
    
    count = 0
    for p in products_data:
        product, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults=p
        )
        if created:
            count += 1
            print(f'✅ Product created: {product.name}')
    
    print(f'\n🎉 {count} new products added successfully!')
    print(f'📦 Total products: {Product.objects.count()}')

if __name__ == '__main__':
    add_products()
