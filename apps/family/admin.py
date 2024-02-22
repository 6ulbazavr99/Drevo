from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.family.models import Family, FamilyMember

admin.site.register(Family, MPTTModelAdmin)
admin.site.register(FamilyMember)
