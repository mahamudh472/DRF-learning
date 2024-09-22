from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name