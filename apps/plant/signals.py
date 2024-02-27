from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PlantedTree


def send_tree_care_email(user, conditions):
    subject = 'Семейное Древо: Уход за деревом'
    base_message = f'Уважаемый {user.username}, вашему дереву требуется уход:\n'

    messages = {
        'watering': 'Требуется поливка.',
        'pruning': 'Требуется обрезка.',
        'fertilizing': 'Требуется подкормка.'
    }

    care_messages = [messages[condition] for condition in conditions if condition in messages]
    message = base_message + "\n".join(care_messages)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


@receiver(pre_save, sender=PlantedTree)
def set_old_needs(sender, instance, **kwargs):
    if instance.pk:
        try:
            current_instance = sender.objects.get(pk=instance.pk)
            instance._old_needs = current_instance.needs
        except sender.DoesNotExist:
            instance._old_needs = []


@receiver(post_save, sender=PlantedTree)
def check_needs_change_and_send_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Поздравляем с посадкой вашего дерева!'
        message = (f'Уважаемый {instance.user.username}, мы рады сообщить, что ваше дерево успешно посажено. '
                   f'Желаем ему расти здоровым и крепким!')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.user.email], fail_silently=False)
    old_needs = getattr(instance, '_old_needs', [])
    if set(old_needs) != set(instance.needs):
        conditions = list(set(instance.needs) - set(old_needs))
        if conditions and instance.user:
            send_tree_care_email(instance.user, conditions)
