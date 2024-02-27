from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from config import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        subject = 'Восстановление пароля "Семейное Древо"'
        token = reset_password_token.key
        message = f'''Здравствуйте, {reset_password_token.user.first_name} {reset_password_token.user.last_name}!

Для сброса вашего пароля, пожалуйста, используйте следующий код на нашем сайте:

{token}

Введите этот код для сброса пароля и задайте новый пароль.

Если вы не запрашивали сброс пароля, пожалуйста, проигнорируйте это письмо.
'''
        from_email = settings.EMAIL_HOST_USER
        to_email = reset_password_token.user.email
        send_mail(subject, message, from_email, [to_email])
    except Exception as e:
        print(f"Ошибка при отправке письма для сброса пароля: {e}")
