import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import Users, Semester
from django.contrib import messages

@pytest.mark.django_db
class TestDeleteUserIntegration:

    @pytest.fixture
    def create_semester(self, db):
        """Crea un semestre de prueba."""
        return Semester.objects.create(semester='Semestre 1')

    @pytest.fixture
    def create_superuser(self, db, create_semester):
        """Crea un superusuario para las pruebas."""
        User = get_user_model()
        user = User.objects.create_superuser(
            username='superuser',
            password='testpass',
            email='superuser@example.com',
            semester=create_semester  # Asigna un semestre válido
        )
        return user

    @pytest.fixture
    def create_user_to_delete(self, db, create_semester):
        """Crea un usuario que se va a eliminar."""
        User = get_user_model()
        user = User.objects.create_user(
            username='user_to_delete',
            password='testpass',
            email='user_to_delete@example.com',
            semester=create_semester  # Asegúrate de que el semestre es válido
        )
        return user

    def test_delete_user_success(self, client, create_superuser, create_user_to_delete):
        """Prueba para eliminar un usuario exitosamente."""
        client.login(username='superuser', password='testpass')

        response = client.post(reverse('delete_users', args=[create_user_to_delete.id]))

        assert response.status_code == 302  # Verifica que redirige después de eliminar
        assert not Users.objects.filter(id=create_user_to_delete.id).exists()  # Verifica que el usuario ha sido eliminado

        # Verifica que se ha creado un mensaje en la siguiente respuesta
        response = client.get(reverse('usuarios'))  # Asumiendo que redirige a una vista donde se puede ver mensajes
        messages_list = list(messages.get_messages(response.wsgi_request))
        assert any(msg.message == 'El usuario se ha eliminado correctamente.' for msg in messages_list)  # Verifica que existe el mensaje

    def test_delete_user_not_exist(self, client, create_superuser):
        """Prueba para intentar eliminar un usuario que no existe."""
        client.login(username='superuser', password='testpass')

        response = client.post(reverse('delete_users', args=[999]))  # Suponiendo que el ID 999 no existe

        assert response.status_code == 302  # Verifica que redirige después del intento

        # Verifica que se ha creado un mensaje en la siguiente respuesta
        response = client.get(reverse('usuarios'))  # Asumiendo que redirige a una vista donde se puede ver mensajes
        messages_list = list(messages.get_messages(response.wsgi_request))
        assert any(msg.message == 'El usuario no existe.' for msg in messages_list)  # Verifica mensaje de error

    def test_delete_user_without_permission(self, client, create_user_to_delete):
        """Prueba para intentar eliminar un usuario sin permiso."""
        # Aquí se debería crear otro tipo de usuario que no tenga permisos para eliminar
        client.logout()  # Asegúrate de que el usuario está desconectado

        response = client.post(reverse('delete_users', args=[create_user_to_delete.id]))

        assert response.status_code == 302  # Verifica que se deniega el acceso sin permisos
