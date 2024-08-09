import datetime
import os
import time

import json
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from .models import Post, Category


@shared_task
def printer():
    for i in range(1, 10):
        time.sleep(1)
        print(f'krakozyabra{i}')

@shared_task
def send_last_weak_post():
    print('task_start')
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_add__gte=last_week)
    print(posts)
    categories = set(posts.values_list('categories__name', flat=True))
    print(categories)
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    print(subscribers)

    html_content = render_to_string(
        'mail_messages_weeksend.html',
        {
            'link': os.getenv("SITE_URL"),
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Добавленные посты за последнюю неделю:',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_mail_new_post(pk, post_type, title, text, subs):
    html_content = render_to_string(
        'mail_message_post_add.html',
        {
            'title': title,
            'text': text,
            'link': f'{os.getenv("SITE_URL")}/{"articles" if post_type == "ART" else "news"}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'NEW POST fromCelery: {title}',
        body='',
        from_email=os.getenv("DEFAULT_FROM_EMAIL"),
        to=subs,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def notify_about_new_post(json_str):
    print(json_str)
    json_str_to_json = json.loads(json_str)
    print(json_str_to_json['post_name'])
    print("-----")
    time.sleep(3)
    post = Post.objects.get(id=json_str_to_json['id'])
    print(post)
    print("-----")
    categories = Post.objects.get(post_name=json_str_to_json['post_name']).categories.all()
    print(categories)
    subscribers_emails = []
    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [adr.email for adr in subscribers]

        print(subscribers)
        print(subscribers_emails, 'task_print')
    print('asd ')
    set_subs = set(subscribers_emails)
    print(set_subs)
    send_mail_new_post(json_str_to_json["id"],
                       json_str_to_json["post_type"],
                       json_str_to_json["post_name"],
                       json_str_to_json["post_text"],
                       set_subs
                       )



