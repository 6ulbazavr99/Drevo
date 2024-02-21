from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.family.models import Family, FamilyTree


@receiver(m2m_changed, sender=Family.parents.through)
def update_family_name(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.set_family_name()
        instance.save()


@receiver(post_save, sender=Family)
def create_family_tree(sender, instance, created, **kwargs):
    if created and not instance.tree:
        family_tree = FamilyTree.objects.create()
        instance.tree = family_tree
        instance.save()
