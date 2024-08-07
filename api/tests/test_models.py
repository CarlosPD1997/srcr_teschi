# import pytest
# from django.core.exceptions import ValidationError
# from api.models import Semester, Classes, Users, requisicion, utensilios

# @pytest.mark.django_db
# class TestModels:

#     def test_semester_creation(self):
#         semester = Semester.objects.create(semester='2024-1')
#         assert semester.semester == '2024-1'
#         assert semester.id is not None

#     def test_classes_creation(self):
#         semester = Semester.objects.create(semester='2024-1')
#         classes = Classes.objects.create(semester=semester, name='Matemáticas')
#         assert classes.name == 'Matemáticas'
#         assert classes.semester == semester
#         assert classes.id is not None

#     def test_users_creation(self):
#         semester = Semester.objects.create(semester='2024-1')
#         user = Users.objects.create_user(
#             username='testuser',
#             password='testpass',
#             email='testuser@example.com',
#             semester=semester
#         )
#         assert user.username == 'testuser'
#         assert user.email == 'testuser@example.com'
#         assert user.semester == semester
#         assert user.id is not None

#     def test_requisicion_creation(self):
#         semester = Semester.objects.create(semester='2024-1')
#         classes = Classes.objects.create(semester=semester, name='Matemáticas')
#         user = Users.objects.create_user(
#             username='testuser',
#             password='testpass',
#             email='testuser@example.com',
#             semester=semester
#         )
#         requisicion_obj = requisicion.objects.create(
#             codigo='REQ001',
#             asignatura=classes,
#             hora_inicio='08:00',
#             hora_fin='10:00',
#             docente='Prof. Smith',
#             grupo='Grupo A',
#             pdf='path/to/pdf',
#             items={'item1': 1, 'item2': 2}
#         )
#         requisicion_obj.users.add(user)

#         assert requisicion_obj.codigo == 'REQ001'
#         assert requisicion_obj.asignatura == classes
#         assert requisicion_obj.hora_inicio == '08:00'
#         assert requisicion_obj.docente == 'Prof. Smith'
#         assert requisicion_obj.users.count() == 1

#     def test_utensilios_creation(self):
#         utensilio = utensilios.objects.create(
#             nombre='Vaporera',
#             cantidad=10,
#             descripcion='Vaporera de acero',
#             tamaño='Mediana',
#             img='path/to/img'
#         )
#         assert utensilio.nombre == 'Vaporera'
#         assert utensilio.cantidad == 10
#         assert utensilio.descripcion == 'Vaporera de acero'
#         assert utensilio.tamaño == 'Mediana'
#         assert utensilio.id is not None

#     def test_validation_error_on_empty_semester(self):
#         with pytest.raises(ValidationError):
#             semester = Semester(semester='')
#             semester.full_clean()  # This will raise a ValidationError

#     def test_validation_error_on_empty_classes_name(self):
#         semester = Semester.objects.create(semester='2024-1')
#         with pytest.raises(ValidationError):
#             classes = Classes(semester=semester, name='')
#             classes.full_clean()  # This will raise a ValidationError
