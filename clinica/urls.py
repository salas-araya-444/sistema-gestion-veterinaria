from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_clinica'),

    path('api/mascotas/', views.mascotas_list_create, name='mascotas_list_create'),

    path('api/mascotas/<int:pk>/', views.mascota_detail, name='mascota_detail'),

    path('api/propietarios/', views.propietarios_list_create, name='propietarios_list_create'),

    path('api/consultas/', views.consultas_list_create, name='consultas_list_create'),

    path('api/perfil/', views.perfil, name='perfil'),

    path('api/estadisticas/', views.estadisticas, name='estadisticas'),

    path('api/sesion/', views.sesion, name='sesion'),
]