from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from .models import PlantedTree


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition_display', 'needs_display', 'type', 'age', 'preview_display',
                    'address', 'updated_at', 'created_at')
    list_filter = ('condition', 'type', 'updated_at', 'created_at')
    search_fields = ('user__username', 'type', 'address')
    readonly_fields = ('updated_at', 'created_at')

    fieldsets = (
        (None, {'fields': ('user', 'condition', 'needs', 'type', 'age', 'preview', 'address')}),
        ('Временные метки', {'fields': ('updated_at', 'created_at'), 'classes': ('collapse',)})
    )

    def condition_display(self, obj):
        return force_str(obj.get_condition_display())
    condition_display.short_description = _('Состояние')

    def needs_display(self, obj):
        needs = [force_str(dict(PlantedTree.NEEDS_CHOICES).get(need, need)) for need in obj.needs]
        return ', '.join(needs) if needs else 'Нет потребностей'
    needs_display.short_description = _('Потребности')

    def preview_display(self, obj):
        return obj.preview.url if obj.preview else 'Нет изображения'
    preview_display.short_description = _('Изображение')


admin.site.register(PlantedTree, PlantedTreeAdmin)
