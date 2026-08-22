from django.core.management.base import BaseCommand
from apps.products.models import Product, Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **kwargs):
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
                self.stdout.write(self.style.SUCCESS(f'Category created: {category.name}'))
        
        # Get first user as owner
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No user found! Create a superuser first.'))
            return
        
        # Sample products
        products_data = [
            {
                'name': 'Premium SaaS Plan',
                'slug': 'premium-saas-plan',
                'description': 'Full access to all premium features including AI, analytics, and unlimited users.',
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
                'description': 'Advanced features for power users with priority support.',
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
                'description': 'Everything you need to get started with SaaSFlow.',
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
                'description': 'Real-time analytics dashboard with custom reports and insights.',
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
                'description': 'Secure cloud storage with 1TB space and end-to-end encryption.',
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
                'description': 'Complete API management with authentication, rate limiting, and analytics.',
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
                'description': 'Complete full-stack web development course with 40+ hours of content.',
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
                'description': '100+ premium UI components and templates for your next project.',
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
                'description': 'AI-powered email marketing platform with automation and analytics.',
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
                'description': 'Professional security audit with vulnerability scanning and penetration testing.',
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
                self.stdout.write(self.style.SUCCESS(f'Product created: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ {count} new products added!'))
        self.stdout.write(self.style.SUCCESS(f'Total products: {Product.objects.count()}'))
