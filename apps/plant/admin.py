from django.contrib import admin
from .models import PlantedTree
from django.utils.translation import gettext_lazy as _


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'condition_display', 'type', 'age', 'preview_display', 'address', 'updated_at',
                    'created_at')
    list_filter = ('condition', 'type', 'updated_at', 'created_at')
    search_fields = ('user__username', 'type', 'address')
    readonly_fields = ('updated_at', 'created_at')
    fieldsets = (
        (None, {'fields': ('user', 'condition', 'type', 'age', 'preview', 'address')}),
        ('Временные метки', {'fields': ('updated_at', 'created_at'), 'classes': ('collapse',)})
    )

    def condition_display(self, obj):
        return ', '.join(obj.get_condition_display())

    condition_display.short_description = _('Состояние')

    def preview_display(self, obj):
        return obj.preview.url if obj.preview else None

    preview_display.short_description = _('Изображение')


admin.site.register(PlantedTree, PlantedTreeAdmin)
