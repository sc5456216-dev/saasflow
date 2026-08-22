import os
import django
import urllib.request
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product, Category
from django.contrib.auth.models import User

# Product images from Unsplash (free stock photos)
PRODUCT_IMAGES = {
    'premium-saas-plan': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop',
    'pro-plan': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=400&fit=crop',
    'starter-kit': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=400&fit=crop',
    'analytics-dashboard-pro': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop',
    'cloud-storage-pro': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=400&fit=crop',
    'api-management-suite': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=400&fit=crop',
    'web-dev-bootcamp': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=400&fit=crop',
    'design-system-templates': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&h=400&fit=crop',
    'email-marketing-pro': 'https://images.unsplash.com/photo-1526378722484-bd91ca387e72?w=400&h=400&fit=crop',
    'security-audit-service': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=400&fit=crop',
}

# Product Icons (FontAwesome classes)
PRODUCT_ICONS = {
    'premium-saas-plan': 'fa-crown',
    'pro-plan': 'fa-rocket',
    'starter-kit': 'fa-box-open',
    'analytics-dashboard-pro': 'fa-chart-line',
    'cloud-storage-pro': 'fa-cloud',
    'api-management-suite': 'fa-code',
    'web-dev-bootcamp': 'fa-laptop-code',
    'design-system-templates': 'fa-paint-brush',
    'email-marketing-pro': 'fa-envelope',
    'security-audit-service': 'fa-shield-alt',
}

def download_image(url):
    """Download image from URL and return a temporary file"""
    try:
        temp_img = NamedTemporaryFile(delete=True, suffix='.jpg')
        urllib.request.urlretrieve(url, temp_img.name)
        return temp_img
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def add_products():
    # Create categories with icons
    categories_data = [
        {'name': 'Software', 'slug': 'software', 'icon': 'fa-code'},
        {'name': 'Services', 'slug': 'services', 'icon': 'fa-cogs'},
        {'name': 'Templates', 'slug': 'templates', 'icon': 'fa-paint-brush'},
        {'name': 'Courses', 'slug': 'courses', 'icon': 'fa-graduation-cap'},
        {'name': 'Tools', 'slug': 'tools', 'icon': 'fa-tools'},
    ]
    
    categories = []
    for cat in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat['slug'],
            defaults={
                'name': cat['name'],
                'icon': cat['icon']
            }
        )
        categories.append(category)
        if created:
            print(f'✅ Category created: {category.name} with icon {category.icon}')
    
    # Products with real images and icons
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
            'category': categories[0],
            'image_url': PRODUCT_IMAGES.get('premium-saas-plan'),
            'icon': '👑'
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
            'category': categories[0],
            'image_url': PRODUCT_IMAGES.get('pro-plan'),
            'icon': '🚀'
        },
        {
            'name': 'Starter Kit',
            'slug': 'starter-kit',
            'description': 'Everything you need to get started with SaaSFlow. Includes basic features, email support, and 5 team members.',
            'short_description': 'Complete starter package',
            'price': 29.99,
            'stock': 500,
            'is_featured': False,
            'status': 'published',
            'is_active': True,
            'category': categories[0],
            'image_url': PRODUCT_IMAGES.get('starter-kit'),
            'icon': '📦'
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
            'category': categories[0],
            'image_url': PRODUCT_IMAGES.get('analytics-dashboard-pro'),
            'icon': '📊'
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
            'category': categories[1],
            'image_url': PRODUCT_IMAGES.get('cloud-storage-pro'),
            'icon': '☁️'
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
            'category': categories[4],
            'image_url': PRODUCT_IMAGES.get('api-management-suite'),
            'icon': '🔌'
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
            'category': categories[3],
            'image_url': PRODUCT_IMAGES.get('web-dev-bootcamp'),
            'icon': '💻'
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
            'category': categories[2],
            'image_url': PRODUCT_IMAGES.get('design-system-templates'),
            'icon': '🎨'
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
            'category': categories[0],
            'image_url': PRODUCT_IMAGES.get('email-marketing-pro'),
            'icon': '✉️'
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
            'category': categories[1],
            'image_url': PRODUCT_IMAGES.get('security-audit-service'),
            'icon': '🛡️'
        }
    ]
    
    count = 0
    for p in products_data:
        product, created = Product.objects.get_or_create(
            slug=p['slug'],
            defaults={
                'name': p['name'],
                'description': p['description'],
                'short_description': p['short_description'],
                'price': p['price'],
                'compare_price': p.get('compare_price'),
                'stock': p['stock'],
                'is_featured': p['is_featured'],
                'status': p['status'],
                'is_active': p['is_active'],
                'category': p['category']
            }
        )
        
        if created:
            count += 1
            # Download and assign image
            if p.get('image_url'):
                temp_file = download_image(p['image_url'])
                if temp_file:
                    product.image.save(f"{product.slug}.jpg", File(temp_file), save=True)
                    print(f'✅ Product created with image: {product.name} {p["icon"]}')
                else:
                    print(f'⚠️ Product created without image: {product.name} {p["icon"]}')
            else:
                print(f'✅ Product created: {product.name} {p["icon"]}')
    
    print(f'\n🎉 {count} new products added successfully!')
    print(f'📦 Total products: {Product.objects.count()}')

if __name__ == '__main__':
    add_products()
