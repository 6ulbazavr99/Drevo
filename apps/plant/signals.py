from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlantedTree


@receiver(post_save, sender=PlantedTree)
def tree_condition_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Если это создание нового дерева, можно отправить уведомление о новом дереве
        pass
    else:
        # Здесь можно проверять изменения в состоянии дерева
        if instance.condition_changed():  # предположим, у вас есть метод для определения изменения состояния
            message = f"Состояние вашего дерева '{instance}' изменилось: {instance.get_condition_display()}"
            # Отправьте это сообщение пользователю
            send_tree_condition_message(instance.user, message)


def send_tree_condition_message(user, message):
    # Реализуйте логику отправки сообщения пользователю
    pass
