from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField


User = get_user_model()


def validate_max_choices(value):
    max_choices = 4
    if len(value) > max_choices:
        raise ValidationError(_('Максимальное количество выбранных значений: %(max_choices)s') %
                              {'max_choices': max_choices})


class PlantedTree(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planted_trees',
                             verbose_name=_("Пользователь"), blank=True, null=True)

    CONDITION_CHOICES = [
        ('good', _('Хорошо')),
        ('medium', _('Средне')),
        ('bad', _('Плохо')),
        ('terrible', _('Ужасное')),
    ]

    NEEDS_CHOICES = [
        ('watering', _('Требуется полить')),
        ('pruning', _('Требуется обрезка')),
        ('fertilizing', _('Требуется подкормка')),
    ]

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name=_("Состояние"),
                                 default='good')
    needs = MultiSelectField(choices=NEEDS_CHOICES, verbose_name=_("Потребности"), blank=True,
                             validators=[validate_max_choices])

    type = models.CharField(max_length=255, verbose_name=_("Вид"), blank=True, null=True)
    age = models.IntegerField(_('Возраст'), blank=True, null=True)
    preview = models.ImageField(_('Изображение'), upload_to='planted_tree_preview/', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=_("Адрес"), blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))

    def __str__(self):
        return f'Посаженное дерево №{self.id} [{self.user}]' if self.user else f'Посаженное дерево №{self.id}'

    class Meta:
        verbose_name = _("Посаженное дерево")
        verbose_name_plural = _("Посаженные деревья")
