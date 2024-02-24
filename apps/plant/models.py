from apps.family.models import FamilyMember
from django.db import models
from multiselectfield import MultiSelectField

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_max_choices(value):
    max_choices = 4
    if len(value) > max_choices:
        raise ValidationError(_('Максимальное количество выбранных значений: %(max_choices)s'),
                              params={'max_choices': max_choices})


class PlantedTree(models.Model):
    user = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, blank=True, null=True, related_name='planted_tree')

    CONDITION_CHOICES = [
        ('watering', 'Требуется полить'),
        ('pruning', 'Требуется обрезка'),
        ('fertilizing', 'Требуется подкормка'),
        ('good', 'Хорошо'),
        ('medium', 'Средне'),
        ('bad', 'Плохо'),
    ]
    condition = MultiSelectField(choices=CONDITION_CHOICES, verbose_name=_("Состояние"), blank=True, null=True,
                                 validators=[validate_max_choices])

    type = models.CharField(max_length=255, verbose_name=_("Вид"), blank=True, null=True)
    age = models.IntegerField(_('Возраст'), blank=True, null=True)
    images = models.ImageField(upload_to='planted_tree_images/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))

    def __str__(self):
        if self.user:
            return f'{self.user} {self.user.role} {self.user.family}'
        return f'PlantedTree #{self.id}'
