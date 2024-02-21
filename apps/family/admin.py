from django.contrib import admin

from apps.family.models import Family, FamilyTree, FamilyGarden, Branch, PlantedTree


admin.site.register(Family)
admin.site.register(FamilyTree)
admin.site.register(FamilyGarden)
admin.site.register(Branch)
admin.site.register(PlantedTree)
