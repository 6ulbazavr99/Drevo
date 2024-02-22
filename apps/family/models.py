from django.contrib.auth import get_user_model
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()


class Family(MPTTModel):
    members = models.ManyToManyField(User, through='FamilyMember', related_name='families')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfamilies')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='family_images/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class MPTTMeta(object):
        order_insertion_by = ['name']


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}'s role in {self.family}: {self.role}"
