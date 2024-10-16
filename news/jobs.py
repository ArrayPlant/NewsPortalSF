from django_apscheduler.jobstores import DjangoJobStore, register_job
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Post, Subscriber
from datetime import timedelta

from celery import shared_task
from django.utils import timezone


def send_weekly_newsletters():
    last_week = now() - timedelta(days=7)
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        posts = Post.objects.filter(categories=subscriber.category, published_at__gte=last_week)
        if posts.exists():
            post_links = "\n".join([f"{post.title}: http://127.0.0.1:8000{post.get_absolute_url()}" for post in posts])
            send_mail(
                subject=f'Weekly newsletter for {subscriber.category.name}',
                message=f'Here are the new posts in {subscriber.category.name} from last week:\n{post_links}',
                from_email='noreply@newsportal.com',
                recipient_list=[subscriber.user.email]
            )


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", day_of_week="fri", hour=18, minute=0)
def weekly_job():
    send_weekly_newsletters()


scheduler.start()


@shared_task
def send_new_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = Subscriber.objects.filter(category=post.category)
    for subscriber in subscribers:
        send_mail(
            f'Новая новость в категории {post.category}',
            f'Новость: {post.title}\n\n{post.content}',
            'noreply@newsportal.com',
            [subscriber.email],
        )


@shared_task
def send_weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    subscribers = Subscriber.objects.all()

    if posts.exists():
        for subscriber in subscribers:
            send_mail(
                'Еженедельная рассылка новостей',
                f'Последние новости за неделю:\n\n' + "\n".join([post.title for post in posts]),
                'noreply@newsportal.com',
                [subscriber.email],
            )