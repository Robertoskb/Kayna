from django.db import models
from manage import init_django

init_django()


class MonsterName(models.Model):
    id = models.AutoField(primary_key=True)
    english_name = models.CharField(max_length=30, unique=True)
    portuguese_name = models.CharField(max_length=30, unique=True)
    spanish_name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.english_name


class IslandName(models.Model):
    id = models.AutoField(primary_key=True)
    english_name = models.CharField(max_length=30, unique=True)
    portuguese_name = models.CharField(max_length=30, unique=True)
    spanish_name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.english_name


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.name


class Rarety(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Element(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Monster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    base_name = models.CharField(max_length=30, null=True, blank=True)
    name_translations = models.ForeignKey(
        MonsterName, blank=True, null=True, on_delete=models.SET_NULL)
    rarety = models.ForeignKey(
        Rarety, null=True, blank=True, on_delete=models.SET_NULL)
    _class = models.ForeignKey(
        Class, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='monsters')
    elements = models.ManyToManyField(
        Element, blank=True, related_name='monsters')
    release_date = models.CharField(max_length=12, null=True, blank=True)
    release_version = models.CharField(max_length=5, null=True, blank=True)
    image = models.ImageField(upload_to='monsters/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Island(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    name_translations = models.ForeignKey(
        IslandName, blank=True, null=True, on_delete=models.SET_NULL)
    monsters = models.ManyToManyField(
        Monster, related_name='islands', blank=True)

    def __str__(self):
        return self.name


class Breeding(models.Model):
    id = models.AutoField(primary_key=True)
    monster = models.ForeignKey(
        Monster, related_name='breedings', blank=True,
        null=True, on_delete=models.SET_NULL)

    monster_1 = models.ForeignKey(
        Monster, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='breeding_1')
    monster_2 = models.ForeignKey(
        Monster, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='breeding_2')
    monster_3 = models.ForeignKey(
        Monster, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='breeding_3')

    any_three_monsters = models.BooleanField(default=False)

    island = models.ForeignKey(
        Island, blank=True, null=True, on_delete=models.SET_NULL)

    default_time = models.DurationField(null=True, blank=True)
    enhanced_time = models.DurationField(null=True, blank=True)
