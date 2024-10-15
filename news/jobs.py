from django_apscheduler.jobstores import DjangoJobStore, register_job
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Post, Subscriber
from datetime import timedelta


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
