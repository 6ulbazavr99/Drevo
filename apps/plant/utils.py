from django.core.mail import send_mail
from django.conf import settings


def send_watering_email(user):
    try:
        subject = 'Семейное Древо: Требуется поливка'
        message = f'Уважаемый {user}, вашему дереву требуется поливка!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Ошибка при отправке электронной почты о поливке: {e}")


def send_pruning_email(user):
    try:
        subject = 'Семейное Древо: Требуется обрезка'
        message = f'Уважаемый {user}, вашему дереву требуется обрезка!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Ошибка при отправке электронной почты об обрезке: {e}")


def send_fertilizing_email(user):
    try:
        subject = 'Семейное Древо: Требуется подкормка'
        message = f'Уважаемый {user}, вашему дереву требуется подкормка!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Ошибка при отправке электронной почты о подкормке: {e}")
