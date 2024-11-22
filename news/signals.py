from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from .models import Post, Subscriber

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs.get('action') == 'post_add':
        categories = instance.categories.all()
        for category in categories:
            subscribers = Subscriber.objects.filter(category=category)
            for subscriber in subscribers:
                send_mail(
                    subject=f'New post in {category.name}',
                    message=f'New post "{instance.title}" in {category.name}. Read it here: http://127.0.0.1:8000{reverse("post_detail", args=[instance.id])}',
                    from_email='noreply@newsportal.com',
                    recipient_list=[subscriber.user.email]
                )
