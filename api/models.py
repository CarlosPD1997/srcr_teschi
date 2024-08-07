from django.db import models
from django.contrib.auth.models import AbstractUser

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.CharField(max_length=30)

    class Meta:
        db_table = 'semester'  # Nombre de la tabla en la base de datos

class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'classes'  # Nombre de la tabla en la base de datos

class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=False)
    profile_photo = models.ImageField(upload_to='img/', default='img/profile.jpg')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    grupo = models.CharField(max_length=20, default='0')
   
    # Ajustando related_name para evitar conflictos

    class Meta:
        db_table = 'users'  # Nombre de la tabla en la base de datos

Users.groups.field.remote_field.related_name = 'users_groups'
Users.user_permissions.field.remote_field.related_name = 'users_permissions'

class requisicion(models.Model):  # Asegúrate de que el nombre de la clase empiece con mayúscula
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    asignatura = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True)
    hora_inicio = models.CharField(max_length=100)
    hora_fin = models.CharField(max_length=100)
    docente = models.CharField(max_length=100)
    grupo = models.CharField(max_length=20)
    pdf = models.FileField(upload_to='pdf/')
    users = models.ManyToManyField(Users)
    created_date = models.DateField(auto_now_add=True)
    
    items = models.JSONField()

    def __str__(self):
        return f"Requisicion {self.id}"

    class Meta:
        db_table = 'requisiciones'  # Nombre de la tabla en la base de datos

class utensilios(models.Model):  # Asegúrate de que el nombre de la clase empiece con mayúscula
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    tamaño = models.CharField(max_length=200)
    img = models.ImageField(upload_to='img/', default='img/vaporera.jpg', null=True)

    class Meta:
        db_table = 'utensilios'  # Nombre de la tabla en la base de datos
