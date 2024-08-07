# Generated by Django 4.2.13 on 2024-08-01 04:25

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('profile_photo', models.ImageField(default='img/profile.jpg', upload_to='img/')),
                ('grupo', models.CharField(default='0', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'classes',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('semester', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'semester',
            },
        ),
        migrations.CreateModel(
            name='utensilios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.CharField(max_length=200)),
                ('tamaño', models.CharField(max_length=200)),
                ('img', models.ImageField(default='img/vaporera.jpg', null=True, upload_to='img/')),
            ],
            options={
                'db_table': 'utensilios',
            },
        ),
        migrations.CreateModel(
            name='requisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=10)),
                ('hora_inicio', models.CharField(max_length=100)),
                ('hora_fin', models.CharField(max_length=100)),
                ('docente', models.CharField(max_length=100)),
                ('grupo', models.CharField(max_length=20)),
                ('pdf', models.FileField(upload_to='pdf/')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('items', models.JSONField()),
                ('asignatura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.classes')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'requisiciones',
            },
        ),
        migrations.AddField(
            model_name='classes',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.semester'),
        ),
        migrations.AddField(
            model_name='users',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.semester'),
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
