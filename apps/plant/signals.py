from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PlantedTree


def send_tree_care_email(user, conditions, condition):
    subject = 'Семейное Древо: Уход за деревом'
    base_message = f'Уважаемый {user.username}, вашему дереву требуется уход:\n\n'

    messages = {
        'watering': '⛲️ Требуется поливка: Не забудьте напоить ваше дерево. \nВода - ключ к его здоровью и красоте!\n',
        'pruning': '✂️ Требуется обрезка: Освободите дерево от лишних веток, \nчтобы оно росло сильным и красивым.\n',
        'fertilizing': '🌱 Требуется подкормка: Подкормите ваше дерево, \nчтобы оно получило все '
                       'необходимые питательные вещества для роста.\n'
    }

    care_messages = [messages[condition] for condition in conditions if condition in messages]
    condition_message = f'\nСостояние дерева: {RUSSIAN_CONDITIONS[condition]}\n\n'
    message = base_message + "\n".join(care_messages) + condition_message
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
        message = (f'🎉 Уважаемый {instance.user.username}, мы рады сообщить, что ваше дерево успешно посажено. '
                   f'Желаем ему расти здоровым и крепким! 🌱')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.user.email], fail_silently=False)
    old_needs = getattr(instance, '_old_needs', [])
    if set(old_needs) != set(instance.needs):
        conditions = list(set(instance.needs) - set(old_needs))
        if conditions and instance.user:
            send_tree_care_email(instance.user, conditions, instance.condition)


@receiver(pre_save, sender=PlantedTree)
def update_tree_condition(sender, instance, **kwargs):
    if instance.needs:
        if len(instance.needs) == 1:
            instance.condition = 'medium'
        elif len(instance.needs) == 2:
            instance.condition = 'bad'
        else:
            instance.condition = 'terrible'
    else:
        instance.condition = 'good'


RUSSIAN_CONDITIONS = {
    'good': 'Хорошо',
    'medium': 'Средне',
    'bad': 'Плохо',
    'terrible': 'Ужасно',
}
