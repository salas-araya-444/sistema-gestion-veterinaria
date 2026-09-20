from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Propietario, Mascota
from .serializers import MascotaSerializer, ConsultaVeterinariaSerializer


#-----------------------------------------------------------------------------------------------

# PRUEBAS DE SERIALIZERS
class SerializerTests(APITestCase):

    def setUp(self):
        self.propietario = Propietario.objects.create(
            identificacion='1-1111-1111',
            nombre='Carlos Rodríguez',
            telefono='8888-1111',
            email='carlos@gmail.com'
        )

        self.mascota = Mascota.objects.create(
            nombre='Max',
            especie='Perro',
            raza='Labrador',
            fecha_nacimiento='2021-05-10',
            peso=25.50,
            activo=True,
            propietario=self.propietario
        )

    # Peso 0 debe ser inválido
    def test_mascota_peso_cero_invalido(self):

        datos = {
            'nombre': 'Luna',
            'especie': 'Perro',
            'raza': 'Pastor Alemán',
            'fecha_nacimiento': '2022-01-10',
            'peso': 0,
            'activo': True,
            'propietario': self.propietario.id
        }

        serializer = MascotaSerializer(data=datos)

        self.assertFalse(serializer.is_valid())
        self.assertIn('peso', serializer.errors)

    # Costo negativo debe ser inválido
    def test_consulta_costo_negativo_invalido(self):

        datos = {
            'mascota': self.mascota.id,
            'motivo': 'Revisión general',
            'diagnostico': 'Sin problemas',
            'tratamiento': 'Ninguno',
            'costo': -5000
        }

        serializer = ConsultaVeterinariaSerializer(data=datos)

        self.assertFalse(serializer.is_valid())
        self.assertIn('costo', serializer.errors)

#-----------------------------------------------------------------------------------------------

# PRUEBAS DE AUTENTICACIÓN Y PERMISOS
class AutenticacionTests(APITestCase):

    def setUp(self):

        self.usuario = User.objects.create_user(
            username='operador_test',
            password='ClaveSegura123!'
        )

        self.admin = User.objects.create_user(
            username='admin_test',
            password='ClaveSegura123!',
            is_staff=True
        )

        self.url_perfil = reverse('perfil')
        self.url_estadisticas = reverse('estadisticas')

    # Usuario anónimo no debe acceder al perfil
    def test_perfil_sin_autenticacion(self):

        response = self.client.get(self.url_perfil)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    # Usuario autenticado debe obtener 200
    def test_perfil_usuario_autenticado(self):

        self.client.force_authenticate(user=self.usuario)

        response = self.client.get(self.url_perfil)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # Usuario regular no debe acceder a estadísticas
    def test_estadisticas_usuario_regular(self):

        self.client.force_authenticate(user=self.usuario)

        response = self.client.get(self.url_estadisticas)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # Administrador sí debe acceder a estadísticas
    def test_estadisticas_administrador(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.url_estadisticas)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

#-----------------------------------------------------------------------------------------------
