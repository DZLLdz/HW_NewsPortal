import os

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import PostCategory
from dotenv import load_dotenv

load_dotenv()


def send_mail_new_post(preview, pk, post_type, title, text, subscribers):
    html_content = render_to_string(
        'mail_message_post_add.html',
        {
            'title': title,
            'text': text,
            'link': f'{os.getenv("SITE_URL")}/{"articles" if post_type=="ART" else "news"}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'NEW POST: {title}',
        body='',
        from_email=os.getenv("DEFAULT_FROM_EMAIL"),
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [adr.email for adr in subscribers]
            print(subscribers)
            print(subscribers_emails)

        send_mail_new_post(instance.preview(), instance.pk, instance.post_type, instance.post_name, instance.post_text, subscribers_emails)
        print(instance)
