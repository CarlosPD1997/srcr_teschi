from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import os 
class Semester(models.Model):
    semester = models.CharField(max_length=30)

class Classes(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Users(AbstractUser):
    email = models.EmailField(unique=False)
    profile_photo = models.ImageField(upload_to='img/', default='img/profile.jpg')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    grupo = models.CharField(max_length=20, default=0)

# Ajustando related_name para evitar conflictos
Users.groups.field.remote_field.related_name = 'users_groups'
Users.user_permissions.field.remote_field.related_name = 'users_permissions'

class requisicion(models.Model):
    codigo = models.CharField(max_length=10)
    asignatura = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True)
    hora_inicio = models.CharField(max_length=100)
    hora_fin = models.CharField(max_length=100)
    docente = models.CharField(max_length=100)
    grupo = models.CharField(max_length=20)
    pdf = models.FileField(upload_to='pdf/')
    users = models.ManyToManyField(Users)
    created_date = models.DateField(auto_now_add=True)

class utensilios(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    tamaño = models.CharField(max_length=50)
    img = models.ImageField(upload_to='img/', default='img/vaporera.jpg')