from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email_with_template(subject, template_name, context, to_email, from_email=None):
    """Send email using HTML template"""
    try:
        # Add site URL to context
        context['site_url'] = 'http://localhost:8001'
        context['site_name'] = 'SaaSFlow'
        
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(
            subject=f"[SaaSFlow] {subject}",
            body=plain_message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        'login_url': '/login/',
        'dashboard_url': '/dashboard/',
        'year': 2026,
    }
    return send_email_with_template(
        subject="Welcome to SaaSFlow! 🚀",
        template_name='emails/welcome.html',
        context=context,
        to_email=user.email
    )

def send_order_confirmation_email(order, user):
    """Send order confirmation email"""
    context = {
        'user': user,
        'order': order,
        'order_number': order.order_number,
        'total': order.total_amount,
        'items': order.items.all(),
        'shipping_address': order.shipping_address,
        'status': order.get_status_display(),
        'created_at': order.created_at,
        'dashboard_url': '/orders/',
    }
    return send_email_with_template(
        subject=f"Order #{order.order_number} Confirmed! 🛍️",
        template_name='emails/order_confirmation.html',
        context=context,
        to_email=user.email
    )

def send_payment_receipt_email(user, payment):
    """Send payment receipt email"""
    context = {
        'user': user,
        'payment': payment,
        'amount': payment.amount,
        'currency': payment.currency,
        'payment_method': payment.payment_method,
        'status': payment.status,
        'created_at': payment.created_at,
        'billing_url': '/payment/billing/',
    }
    return send_email_with_template(
        subject="Payment Receipt - SaaSFlow 💳",
        template_name='emails/payment_receipt.html',
        context=context,
        to_email=user.email
    )

def send_password_reset_email(user, reset_link):
    """Send password reset email"""
    context = {
        'user': user,
        'username': user.username,
        'reset_link': reset_link,
        'validity_hours': 24,
        'login_url': '/login/',
    }
    return send_email_with_template(
        subject="Password Reset Request 🔐",
        template_name='emails/password_reset.html',
        context=context,
        to_email=user.email
    )

def send_team_invitation_email(user, team, invited_by):
    """Send team invitation email"""
    context = {
        'user': user,
        'team': team,
        'invited_by': invited_by,
        'company': team.company,
        'team_name': team.name,
        'accept_url': f'/teams/{team.id}/join/',
        'dashboard_url': '/teams/',
    }
    return send_email_with_template(
        subject=f"Team Invitation: {team.name} 👥",
        template_name='emails/team_invitation.html',
        context=context,
        to_email=user.email
    )
