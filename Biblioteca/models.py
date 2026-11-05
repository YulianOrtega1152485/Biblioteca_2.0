from django.db import models

# Create your models here.
class Estudiante(models.Model):
    codigo=models.CharField(max_length=10, blank=False, null=False,unique=True)
    nombre=models.CharField(max_length=100, blank=False, null=False)
    email=models.CharField(max_length=100, blank=False, null=False,unique=True)

def __str__(self):
    return f"{codigo}-{nombre}"

    