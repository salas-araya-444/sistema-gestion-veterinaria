from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Propietario, Mascota, ConsultaVeterinaria
from .serializers import (
    PropietarioSerializer,
    MascotaSerializer,
    ConsultaVeterinariaSerializer
)

#-----------------------------------------------------------------------------------------------

# Vista inicial
def inicio(request):
    return HttpResponse('API de Gestión Veterinaria activa')

#-----------------------------------------------------------------------------------------------

# LISTAR Y CREAR MASCOTAS
@api_view(['GET', 'POST'])
def mascotas_list_create(request):

    if request.method == 'GET':
        mascotas = Mascota.objects.all()

        especie = request.GET.get('especie')
        activas = request.GET.get('activas')
        propietario = request.GET.get('propietario')

        if especie:
            mascotas = mascotas.filter(especie__iexact=especie)

        if activas:
            if activas.lower() == 'true':
                mascotas = mascotas.filter(activo=True)
            elif activas.lower() == 'false':
                mascotas = mascotas.filter(activo=False)

        if propietario:
            mascotas = mascotas.filter(propietario_id=propietario)

        paginator = Paginator(mascotas, 5)
        numero_pagina = request.GET.get('page', 1)
        pagina = paginator.get_page(numero_pagina)

        serializer = MascotaSerializer(pagina, many=True)

        return Response({
            'pagina_actual': pagina.number,
            'total_paginas': paginator.num_pages,
            'total_mascotas': paginator.count,
            'resultados': serializer.data
        })

    if request.method == 'POST':
        serializer = MascotaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

#-----------------------------------------------------------------------------------------------

# OBTENER, ACTUALIZAR Y ELIMINAR UNA MASCOTA
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def mascota_detail(request, pk):

    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'GET':
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = MascotaSerializer(
            mascota,
            data=request.data,
            partial=request.method == 'PATCH'
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        mascota.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

#-----------------------------------------------------------------------------------------------

# LISTAR Y CREAR PROPIETARIOS
@api_view(['GET', 'POST'])
def propietarios_list_create(request):

    if request.method == 'GET':
        propietarios = Propietario.objects.all()
        serializer = PropietarioSerializer(
            propietarios,
            many=True
        )
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PropietarioSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

#-----------------------------------------------------------------------------------------------

# LISTAR Y CREAR CONSULTAS
@api_view(['GET', 'POST'])
def consultas_list_create(request):

    if request.method == 'GET':
        consultas = ConsultaVeterinaria.objects.all()
        serializer = ConsultaVeterinariaSerializer(
            consultas,
            many=True
        )
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ConsultaVeterinariaSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

#-----------------------------------------------------------------------------------------------

# PERFIL DEL USUARIO AUTENTICADO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):

    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })

#-----------------------------------------------------------------------------------------------

# ESTADÍSTICAS SOLO PARA ADMINISTRADORES
@api_view(['GET'])
@permission_classes([IsAdminUser])
def estadisticas(request):

    return Response({
        'total_propietarios': Propietario.objects.count(),
        'total_mascotas': Mascota.objects.count(),
        'mascotas_activas': Mascota.objects.filter(activo=True).count(),
        'total_consultas': ConsultaVeterinaria.objects.count()
    })

#-----------------------------------------------------------------------------------------------

# CONTADOR DE SESIÓN
@api_view(['GET'])
def sesion(request):

    visitas = request.session.get('visitas', 0) + 1
    request.session['visitas'] = visitas

    return Response({
        'visitas_en_esta_sesion': visitas
    })

#-----------------------------------------------------------------------------------------------
