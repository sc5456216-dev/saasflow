# SaaSFlow - Modern SaaS Platform

## 🚀 Features

### Authentication & Users
- User Registration with email
- User Login/Logout
- Password Reset via email
- User Profile with avatar upload
- Email verification (optional)

### Company Management
- Create and manage companies
- Company profile with website
- Active/Inactive company status

### Subscription Plans
- Three tiered plans: Starter, Professional, Enterprise
- Subscribe to plans
- Change/Upgrade plans
- Auto-renewal support

### Dashboard
- User dashboard with company info
- Subscription status
- Quick actions menu
- Usage statistics

### Admin Panel
- Full Django admin interface
- Manage users, companies, subscriptions
- Admin dashboard

### Technical Features
- Docker containerization
- PostgreSQL database
- REST API ready
- Responsive design
- Production-ready settings

## 🛠️ Installation

1. Clone the repository
2. Build Docker containers:
   \\\ash
   docker-compose build
   docker-compose up -d
   \\\
3. Run migrations:
   \\\ash
   docker-compose exec web python manage.py migrate
   \\\
4. Create superuser:
   \\\ash
   docker-compose exec web python manage.py createsuperuser
   \\\
5. Access at http://localhost:8001

## 🗺️ URL Structure

- / - Landing page
- /register/ - User registration
- /login/ - User login
- /logout/ - User logout
- /dashboard/ - User dashboard
- /dashboard/create-company/ - Create company
- /dashboard/plans/ - View subscription plans
- /dashboard/subscribe/<plan_id>/ - Subscribe to plan
- /profile/ - User profile
- /profile/edit/ - Edit profile
- /admin/ - Admin panel
- /api/ - API root

## 📦 Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL 17
- **Container**: Docker & Docker Compose
- **Web Server**: Gunicorn (production)
- **Reverse Proxy**: Nginx (production)
- **Frontend**: HTML, CSS, JavaScript

## 🚀 Production Deployment

1. Create production environment file
2. Use docker-compose.prod.yml
3. Configure SSL/HTTPS
4. Set up domain and DNS
5. Configure email service

## 📝 License

MIT License
