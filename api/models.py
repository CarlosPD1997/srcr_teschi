from django.db import models
from django.contrib.auth.models import AbstractUser

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.CharField(max_length=30)

    class Meta:
        db_table = 'Semestre'  # Nombre de la tabla en la base de datos


class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=False)
    profile_photo = models.ImageField(upload_to='img/', default='img/profile.jpg')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    grupo = models.CharField(max_length=20, default='0')
   
    # Ajustando related_name para evitar conflictos

    class Meta:
        db_table = 'Usuario'  # Nombre de la tabla en la base de datos

Users.groups.field.remote_field.related_name = 'users_groups'
Users.user_permissions.field.remote_field.related_name = 'users_permissions'

class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(Users, related_name='materia_usuario')
    
    class Meta:
        db_table = 'Materia'  # Nombre de la tabla en la base de datos

class Talleres(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(Users, related_name='taller_usuario')
    
    class Meta:
        db_table = 'Taller'  # Nombre de la tabla en la base de datos


class requisicion(models.Model):  # Asegúrate de que el nombre de la clase empiece con mayúscula
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    asignatura = models.ForeignKey(
        'Classes', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='requisiciones_asignatura'  # Unique related_name for this ForeignKey
    )
    taller = models.ForeignKey(
        'Talleres', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='requisiciones_taller'  # Unique related_name for this ForeignKey
    )
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
        db_table = 'Requisicion'  # Nombre de la tabla en la base de datos

class utensilios(models.Model):  # Asegúrate de que el nombre de la clase empiece con mayúscula
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    tamaño = models.CharField(max_length=200)
    img = models.ImageField(upload_to='img/', default='img/vaporera.jpg', null=True)
    solicitudes = models.IntegerField(default=0)

    class Meta:
        db_table = 'Utensilio'  # Nombre de la tabla en la base de datos

    def incrementar_solicitud(self):
        """Incrementa el contador de solicitudes en 1 y guarda el cambio."""
        self.solicitudes += 1
        self.save()  # Guarda los cambios en la base de datos