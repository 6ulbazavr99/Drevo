from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class FamilyTree(models.Model):
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='tree_images/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            family = Family.objects.get(tree=self)
            return family.family_name
        except Family.DoesNotExist:
            return f'Семейное древо №{self.pk}'
        except Exception as e:
            return f'Ошибка: {str(e)}'


class Branch(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='branch')
    role = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class PlantedTree(models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, blank=True, null=True, related_name='planted_tree')
    images = models.ImageField(upload_to='planted_tree_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.branch.user)


class FamilyGarden(models.Model):
    family_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    trees = models.ManyToManyField(FamilyTree, related_name='family_gardens', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.family_name


class Family(models.Model):
    parents = models.ManyToManyField(User, related_name='parent_families', blank=True)
    children = models.ManyToManyField(User, related_name='child_families', blank=True)
    tree = models.OneToOneField(FamilyTree, on_delete=models.SET_NULL, blank=True, null=True, related_name='family')

    family_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='family_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_family_name(self):
        father = self.parents.filter(profile__gender='male').first()
        mother = self.parents.filter(profile__gender='female').first()

        if father and father.last_name:
            self.family_name = father.last_name
        elif mother and mother.last_name:
            self.family_name = mother.last_name

    def __str__(self):
        if self.family_name:
            return self.family_name
        else:
            return f'Семья №{self.pk}'
