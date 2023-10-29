from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Course, Subscription
from users.models import User


@shared_task
def send_update_notification(course_pk):
    checked_time = datetime.utcnow() - timedelta(hours=4)
    course = Course.objects.get(pk=course_pk)
    lessons = course.lesson_set.filter(date_of_last_modification__lt=checked_time).count()

    if lessons >= 0 or course.date_of_last_modification < checked_time:
        users = Subscription.objects.filter(course_id=course_pk).values("user_id")
        emails = User.objects.filter(pk__in=users).values("email")

        send_mail(
            subject=f"Обновление курса",
            message=f"Курс {course.title} - обновился!",
            recipient_list=[email["email"] for email in emails],
            from_email=settings.EMAIL_HOST_USER,
            fail_silently=False
        )

@shared_task
def check_by_login_date():
    check_date = datetime.utcnow() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=check_date)

    for user in users:
        user.is_active = False
        user.save()
