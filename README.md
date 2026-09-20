# Sistema de Gestión Veterinaria

Proyecto desarrollado para el curso **IF0009 - Desarrollo de Software IV** de la **Universidad de Costa Rica, Sede del Pacífico**.

**Autor:** Esteban Salas Araya (C5J444)

---

## 1. Descripción

Este proyecto implementa el backend de una clínica veterinaria utilizando **Django** y **Django REST Framework**.

El sistema permite administrar:

- Propietarios.
- Mascotas.
- Consultas veterinarias.
- Paginación y filtros.
- Autenticación mediante tokens.
- Permisos para usuarios autenticados y administradores.
- Sesiones.
- Pruebas automatizadas.
- Pruebas manuales mediante Postman.

---

## 2. Tecnologías utilizadas

- Python
- Django 5.2
- Django REST Framework
- SQLite
- TokenAuthentication
- Postman
- Git y GitHub

Las versiones exactas instaladas se encuentran en `requirements.txt`.

---

## 3. Estructura principal del proyecto

```text
sistema-gestion-veterinaria/
│
├── clinica/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── veterinaria_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── postman/
│   └── Sistema-Gestion-Veterinaria.postman_collection.json
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

---

## 4. Instalación

### 4.1 Clonar el repositorio

```bash
git clone https://github.com/salas-araya-444/sistema-gestion-veterinaria.git
cd sistema-gestion-veterinaria
```

### 4.2 Crear el entorno virtual

En Windows:

```powershell
python -m venv .venv
```

### 4.3 Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4.4 Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

---

## 5. Base de datos y migraciones

Crear migraciones, si fueran necesarias:

```powershell
python manage.py makemigrations
```

Aplicar las migraciones:

```powershell
python manage.py migrate
```

El proyecto utiliza SQLite durante el desarrollo.

---

## 6. Acceso para evaluación

Por seguridad, **el repositorio no incluye contraseñas reales ni tokens de autenticación**.

Para probar los endpoints protegidos, la persona evaluadora puede crear sus propios usuarios localmente.

### 6.1 Crear un administrador

Ejecutar:

```powershell
python manage.py createsuperuser
```

Django solicitará:

```text
Username:
Email address:
Password:
Password (again):
```

El usuario creado tendrá permisos de administrador y podrá utilizar el endpoint de estadísticas.

### 6.2 Crear un usuario regular

Primero iniciar el servidor:

```powershell
python manage.py runserver
```

Entrar al panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

Iniciar sesión con el superusuario creado anteriormente y luego ir a:

```text
Authentication and Authorization
→ Users
→ Add user
```

Crear un usuario normal y asegurarse de que **Staff status** y **Superuser status** permanezcan desmarcados.

Ese usuario servirá para comprobar:

- Acceso correcto a `/clinica/api/perfil/`.
- Rechazo de acceso a `/clinica/api/estadisticas/`.

### 6.3 Obtener un token

Una vez creados los usuarios:

```text
POST http://127.0.0.1:8000/api/token/
```

Body JSON:

```json
{
    "username": "USUARIO",
    "password": "CONTRASENA"
}
```

La respuesta tendrá la forma:

```json
{
    "token": "TOKEN_GENERADO"
}
```

Luego se envía en las solicitudes protegidas mediante:

```text
Authorization: Token TOKEN_GENERADO
```

> Los tokens de prueba y las contraseñas no se guardan en Git ni en la colección exportada de Postman.

---

## 7. Ejecutar el proyecto

Iniciar el servidor de desarrollo:

```powershell
python manage.py runserver
```

Servidor local:

```text
http://127.0.0.1:8000/
```

Ruta inicial:

```text
http://127.0.0.1:8000/clinica/
```

Respuesta esperada:

```text
API de Gestión Veterinaria activa!
```

---

## 8. Modelos

### Propietario

Campos principales:

- `identificacion`
- `nombre`
- `telefono`
- `email`

Un propietario puede tener varias mascotas.

### Mascota

Campos principales:

- `nombre`
- `especie`
- `raza`
- `fecha_nacimiento`
- `peso`
- `activo`
- `propietario`

Cada mascota pertenece a un propietario.

Validaciones principales:

- El peso debe ser mayor que `0`.
- El nombre no puede estar vacío.

### ConsultaVeterinaria

Campos principales:

- `mascota`
- `fecha`
- `motivo`
- `diagnostico`
- `tratamiento`
- `costo`

Cada consulta veterinaria pertenece a una mascota.

Validaciones principales:

- El costo no puede ser negativo.
- El motivo es obligatorio.

---

## 9. Datos utilizados durante las pruebas

Durante el desarrollo se verificó el sistema con, como mínimo:

- 4 propietarios.
- 8 mascotas.
- 8 consultas veterinarias.

Si se utiliza una base de datos nueva, estos datos pueden cargarse desde el panel administrativo de Django.

Para probar correctamente la segunda página de la paginación deben existir más de 5 mascotas.

---

## 10. Endpoints

| Método | URL | Descripción | Parámetros / Body | Respuestas principales |
|---|---|---|---|---|
| GET | `/clinica/` | Comprobar que la aplicación está activa | Ninguno | 200 |
| GET | `/clinica/api/mascotas/` | Listar mascotas | Query params opcionales | 200 |
| POST | `/clinica/api/mascotas/` | Crear una mascota | JSON | 201, 400 |
| GET | `/clinica/api/mascotas/<id>/` | Obtener una mascota | ID | 200, 404 |
| PUT | `/clinica/api/mascotas/<id>/` | Actualizar completamente una mascota | JSON | 200, 400, 404 |
| PATCH | `/clinica/api/mascotas/<id>/` | Actualizar parcialmente una mascota | JSON | 200, 400, 404 |
| DELETE | `/clinica/api/mascotas/<id>/` | Eliminar una mascota | ID | 204, 404 |
| GET | `/clinica/api/propietarios/` | Listar propietarios | Ninguno | 200 |
| POST | `/clinica/api/propietarios/` | Crear un propietario | JSON | 201, 400 |
| GET | `/clinica/api/consultas/` | Listar consultas | Ninguno | 200 |
| POST | `/clinica/api/consultas/` | Crear una consulta | JSON | 201, 400 |
| POST | `/api/token/` | Obtener token | Username y password | 200, 400 |
| GET | `/clinica/api/perfil/` | Perfil del usuario autenticado | Token | 200, 401 |
| GET | `/clinica/api/estadisticas/` | Estadísticas administrativas | Token de administrador | 200, 401, 403 |
| GET | `/clinica/api/sesion/` | Contador de sesión | Ninguno | 200 |

---

## 11. Paginación

El endpoint de mascotas utiliza una paginación de **5 registros por página**.

Ejemplo:

```text
GET /clinica/api/mascotas/?page=2
```

La respuesta contiene:

```json
{
    "pagina_actual": 2,
    "total_paginas": 2,
    "total_mascotas": 8,
    "resultados": []
}
```

La cantidad exacta de páginas y registros dependerá de los datos almacenados en la base de datos.

---

## 12. Filtros

### Filtrar por especie

```text
GET /clinica/api/mascotas/?especie=Perro
```

### Filtrar por estado activo

```text
GET /clinica/api/mascotas/?activas=true
```

También se puede utilizar:

```text
GET /clinica/api/mascotas/?activas=false
```

### Filtrar por propietario

```text
GET /clinica/api/mascotas/?propietario=1
```

### Combinar filtros

```text
GET /clinica/api/mascotas/?especie=Perro&activas=true
```

---

## 13. Autenticación y permisos

El proyecto utiliza:

```text
TokenAuthentication
```

### Perfil

Endpoint:

```text
GET /clinica/api/perfil/
```

Permiso utilizado:

```text
IsAuthenticated
```

Cualquier usuario autenticado mediante un token válido puede acceder.

La respuesta contiene:

```json
{
    "id": 1,
    "username": "usuario",
    "email": ""
}
```

### Estadísticas

Endpoint:

```text
GET /clinica/api/estadisticas/
```

Permiso utilizado:

```text
IsAdminUser
```

Un usuario regular autenticado recibe un rechazo de acceso.

Un administrador puede acceder y recibe información como:

```json
{
    "total_propietarios": 4,
    "total_mascotas": 8,
    "mascotas_activas": 7,
    "total_consultas": 8
}
```

Los valores dependen de la información almacenada en la base de datos.

---

## 14. Sesiones

Endpoint:

```text
GET /clinica/api/sesion/
```

Se utiliza `request.session` para mantener un contador de visitas.

Primera solicitud:

```json
{
    "visitas_en_esta_sesion": 1
}
```

Segunda solicitud desde la misma sesión:

```json
{
    "visitas_en_esta_sesion": 2
}
```

El contador continúa aumentando mientras se conserve la misma sesión.

---

## 15. ORM de Django

Durante el desarrollo se utilizaron consultas ORM para:

- Listar todas las mascotas.
- Ordenar mascotas por nombre.
- Obtener mascotas activas.
- Obtener mascotas con peso mayor a 10.
- Filtrar mascotas por especie.
- Buscar propietarios por nombre.
- Consultar relaciones entre propietarios y mascotas.
- Actualizar registros.
- Eliminar registros.

Ejemplo:

```python
Mascota.objects.filter(peso__gt=10)
```

`gt` significa **greater than**, es decir, “mayor que”.

El doble guion bajo `__` permite aplicar lookups de Django sobre un campo.

---

## 16. Pruebas automatizadas

Ejecutar:

```powershell
python manage.py test
```

El proyecto contiene 6 pruebas automatizadas:

1. Una mascota con peso `0` es inválida.
2. Una consulta con costo negativo es inválida.
3. Un usuario anónimo no puede acceder a `/perfil/`.
4. Un usuario autenticado puede acceder a `/perfil/`.
5. Un usuario regular no puede acceder a `/estadisticas/`.
6. Un administrador puede acceder a `/estadisticas/`.

Resultado obtenido durante el desarrollo:

```text
Found 6 test(s).
......
----------------------------------------------------------------------
Ran 6 tests

OK
```

---

## 17. Pruebas con Postman

La colección exportada se encuentra en:

```text
postman/Sistema-Gestion-Veterinaria.postman_collection.json
```

Para utilizarla:

1. Abrir Postman.
2. Seleccionar **Import**.
3. Importar el archivo `.postman_collection.json`.
4. Iniciar el servidor de Django.
5. Ejecutar las solicitudes de la colección.

La colección incluye los 13 casos principales de prueba:

1. GET para listar mascotas.
2. POST de una mascota válida.
3. POST con peso `0`.
4. GET de una mascota inexistente.
5. PATCH para actualizar una mascota.
6. GET de la página 2.
7. GET filtrando por especie.
8. POST de una consulta con costo negativo.
9. GET de perfil sin token.
10. GET de perfil con token.
11. GET de estadísticas con usuario regular.
12. GET de estadísticas con administrador.
13. DELETE de una mascota.

La colección utiliza marcadores como:

```text
Token TU_TOKEN_AQUI
```

y:

```text
TU_CONTRASENA_AQUI
```

para evitar almacenar credenciales reales.

---

## 18. Reflexión final

### Autenticación y autorización

La autenticación responde a la pregunta: **¿quién es el usuario?**

En este proyecto se utiliza `TokenAuthentication`. El usuario proporciona sus credenciales a `/api/token/` y recibe un token que posteriormente utiliza para identificarse ante la API.

La autorización responde a la pregunta: **¿qué puede hacer ese usuario?**

Esto puede observarse en los endpoints `/perfil/` y `/estadisticas/`.

`/perfil/` utiliza `IsAuthenticated`, por lo que cualquier usuario que se haya autenticado correctamente puede acceder.

`/estadisticas/` utiliza `IsAdminUser`. Por lo tanto, aunque un usuario regular tenga un token válido, no puede acceder a esa información porque no cuenta con permisos administrativos.

### Sesiones y HTTP

HTTP es un protocolo sin estado, por lo que cada solicitud es independiente y el servidor no recuerda automáticamente las solicitudes anteriores.

Django permite mantener información entre solicitudes mediante sesiones. El cliente conserva una identificación de sesión y Django utiliza esa identificación para recuperar los datos correspondientes.

Por esta razón, `/clinica/api/sesion/` puede mantener un contador de visitas para un mismo cliente aunque cada solicitud HTTP sea independiente.

### Organización de URLs

Las rutas específicas de la aplicación se encuentran en `clinica/urls.py`.

El archivo `veterinaria_backend/urls.py` se utiliza principalmente para incluir las rutas generales del proyecto, como el panel administrativo, la aplicación `clinica` y la obtención de tokens.

Esta separación facilita la organización y el mantenimiento del proyecto.

---

## 19. Seguridad

El repositorio no debe incluir:

- Contraseñas reales.
- Tokens reales.
- Archivos `.env`.
- Entornos virtuales `.venv`.
- Archivos `__pycache__`.
- Archivos `.pyc`.

Las credenciales necesarias para evaluar el proyecto deben crearse localmente siguiendo la sección **Acceso para evaluación**.

---

## 20. Autor

**Esteban Salas Araya (C5J444)**  
Universidad de Costa Rica, Sede del Pacífico
IF0009 - Desarrollo de Software IV
