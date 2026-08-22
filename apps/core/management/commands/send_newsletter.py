from django.core.management.base import BaseCommand
from apps.core.models import Newsletter
from apps.core.utils.email_utils import send_email_with_template

class Command(BaseCommand):
    help = 'Send newsletter to all subscribers'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str, help='Newsletter subject')
        parser.add_argument('content', type=str, help='Newsletter content')

    def handle(self, *args, **options):
        subscribers = Newsletter.objects.filter(is_active=True)
        subject = options['subject']
        content = options['content']
        
        if not subscribers.exists():
            self.stdout.write(self.style.WARNING('No subscribers found.'))
            return
        
        count = 0
        for subscriber in subscribers:
            context = {
                'email': subscriber.email,
                'content': content,
                'subject': subject,
            }
            send_email_with_template(
                subject=subject,
                template_name='emails/newsletter.html',
                context=context,
                to_email=subscriber.email
            )
            count += 1
            self.stdout.write(f'Sent to {subscriber.email}')
        
        self.stdout.write(self.style.SUCCESS(f'Newsletter sent to {count} subscribers.'))
