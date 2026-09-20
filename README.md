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

El proyecto utiliza **SQLite** durante el desarrollo.

El archivo local `db.sqlite3` no se versiona en Git, por lo que al clonar el proyecto se debe ejecutar `python manage.py migrate` para crear la base de datos local.

---

## 6. Acceso para evaluación

Por seguridad, el repositorio **no incluye contraseñas reales ni tokens de autenticación**.

Para probar los endpoints protegidos, la persona evaluadora puede crear sus propios usuarios localmente.

### 6.1 Crear un usuario administrador

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

El usuario creado tendrá permisos de administrador y podrá acceder al endpoint de estadísticas.

### 6.2 Crear un usuario regular

Primero iniciar el servidor:

```powershell
python manage.py runserver
```

Entrar al panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

Iniciar sesión con el superusuario y crear un usuario normal desde:

```text
Authentication and Authorization
→ Users
→ Add user
```

Para que sea un usuario regular, **Staff status** y **Superuser status** deben permanecer desmarcados.

Este usuario permite comprobar:

- Acceso correcto a `/clinica/api/perfil/`.
- Rechazo de acceso a `/clinica/api/estadisticas/`.

### 6.3 Obtener un token

Solicitud:

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

Respuesta esperada:

```json
{
  "token": "TOKEN_GENERADO"
}
```

El token se utiliza en el header:

```text
Authorization: Token TOKEN_GENERADO
```

> Los tokens y contraseñas reales no se almacenan en Git ni en la colección exportada de Postman.

---

## 7. Ejecutar el proyecto

Iniciar el servidor:

```powershell
python manage.py runserver
```

Servidor local:

```text
http://127.0.0.1:8000/
```

Ruta inicial de la aplicación:

```text
http://127.0.0.1:8000/clinica/
```

Respuesta esperada:

```text
API de Gestión Veterinaria activa
```

---

## 8. Modelos

### Propietario

Campos principales:

- `identificacion`
- `nombre`
- `telefono`
- `email`

Relación:

- Un propietario puede tener varias mascotas.

Reglas principales:

- La identificación es obligatoria.
- El nombre es obligatorio.
- El email es opcional y utiliza `EmailField`.

### Mascota

Campos principales:

- `nombre`
- `especie`
- `raza`
- `fecha_nacimiento`
- `peso`
- `activo`
- `propietario`

Relación:

- Cada mascota pertenece a un propietario mediante `ForeignKey`.
- La relación inversa utiliza `related_name='mascotas'`.

Reglas principales:

- El peso debe ser mayor que `0`.
- El nombre no puede estar vacío.
- El propietario es obligatorio.

### ConsultaVeterinaria

Campos principales:

- `mascota`
- `fecha`
- `motivo`
- `diagnostico`
- `tratamiento`
- `costo`

Relación:

- Cada consulta pertenece a una mascota mediante `ForeignKey`.
- La relación inversa utiliza `related_name='consultas'`.

Reglas principales:

- El costo no puede ser negativo.
- El motivo es obligatorio.
- La fecha se registra automáticamente al crear la consulta.

---

## 9. Datos utilizados durante las pruebas

Durante el desarrollo se verificó el sistema con, como mínimo:

- 4 propietarios.
- 8 mascotas.
- 8 consultas veterinarias.

Si se utiliza una base de datos nueva, estos datos pueden cargarse desde Django Admin.

Para probar correctamente la segunda página de la paginación deben existir más de 5 mascotas.

---

## 10. Documentación de endpoints

| Método | URL | Descripción | Parámetros / Body | Respuesta | Códigos |
|---|---|---|---|---|---|
| GET | `/clinica/` | Verificar que la aplicación está activa | Ninguno | Texto de confirmación | 200 |
| GET | `/clinica/api/mascotas/` | Listar mascotas | Query params opcionales | JSON paginado | 200 |
| POST | `/clinica/api/mascotas/` | Crear una mascota | JSON de mascota | Mascota creada o errores de validación | 201, 400 |
| GET | `/clinica/api/mascotas/<id>/` | Obtener una mascota | ID en la URL | JSON de mascota | 200, 404 |
| PUT | `/clinica/api/mascotas/<id>/` | Actualizar completamente una mascota | JSON completo | Mascota actualizada o errores | 200, 400, 404 |
| PATCH | `/clinica/api/mascotas/<id>/` | Actualizar parcialmente una mascota | JSON parcial | Mascota actualizada o errores | 200, 400, 404 |
| DELETE | `/clinica/api/mascotas/<id>/` | Eliminar una mascota | ID en la URL | Sin contenido | 204, 404 |
| GET | `/clinica/api/propietarios/` | Listar propietarios | Ninguno | Lista JSON | 200 |
| POST | `/clinica/api/propietarios/` | Crear un propietario | JSON de propietario | Propietario creado o errores | 201, 400 |
| GET | `/clinica/api/consultas/` | Listar consultas | Ninguno | Lista JSON | 200 |
| POST | `/clinica/api/consultas/` | Crear una consulta | JSON de consulta | Consulta creada o errores | 201, 400 |
| POST | `/api/token/` | Obtener token de autenticación | `username` y `password` | Token | 200, 400 |
| GET | `/clinica/api/perfil/` | Obtener perfil del usuario autenticado | Header con token | `id`, `username`, `email` | 200, 401 |
| GET | `/clinica/api/estadisticas/` | Obtener estadísticas administrativas | Token de administrador | Totales del sistema | 200, 401, 403 |
| GET | `/clinica/api/sesion/` | Consultar contador de sesión | Ninguno | Contador de accesos | 200 |

---

## 11. Paginación

El listado de mascotas utiliza una paginación de **5 registros por página**.

Ejemplos:

```text
GET /clinica/api/mascotas/?page=1
GET /clinica/api/mascotas/?page=2
```

La respuesta incluye:

```json
{
  "pagina_actual": 2,
  "total_paginas": 2,
  "total_mascotas": 8,
  "resultados": []
}
```

La cantidad exacta de páginas y registros depende de los datos almacenados.

---

## 12. Filtros

### Filtrar por especie

```text
GET /clinica/api/mascotas/?especie=Perro
```

### Filtrar mascotas activas

```text
GET /clinica/api/mascotas/?activas=true
```

También se puede consultar:

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

El proyecto utiliza `TokenAuthentication` de Django REST Framework.

### Perfil

Endpoint:

```text
GET /clinica/api/perfil/
```

Permiso:

```text
IsAuthenticated
```

Cualquier usuario autenticado con un token válido puede acceder.

Ejemplo de respuesta:

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

Permiso:

```text
IsAdminUser
```

Un usuario regular autenticado debe recibir acceso rechazado.

Un administrador puede acceder y recibe información como:

```json
{
  "total_propietarios": 4,
  "total_mascotas": 8,
  "mascotas_activas": 7,
  "total_consultas": 8
}
```

Los valores dependen de los registros existentes en la base de datos.

---

## 14. Sesiones

Endpoint:

```text
GET /clinica/api/sesion/
```

Se utiliza `request.session` para mantener un contador de accesos.

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

A continuación se documentan las consultas ORM solicitadas en la práctica.

```python
# 1. Listar todas las mascotas
Mascota.objects.all()

# 2. Ordenar las mascotas alfabéticamente por nombre
Mascota.objects.all().order_by('nombre')

# 3. Obtener únicamente mascotas activas
Mascota.objects.filter(activo=True)

# 4. Obtener mascotas cuyo peso sea mayor que 10
Mascota.objects.filter(peso__gt=10)

# 5. Buscar mascotas cuya especie sea 'Perro'
Mascota.objects.filter(especie='Perro')

# 6. Buscar propietarios cuyo nombre contenga una palabra
#    sin distinguir mayúsculas y minúsculas
Propietario.objects.filter(nombre__icontains='Carlos')

# 7. Obtener todas las mascotas de un propietario mediante la relación
propietario = Propietario.objects.first()
propietario.mascotas.all()

# 8. Actualizar el peso de una mascota
mascota = Mascota.objects.first()
mascota.peso = 26.00
mascota.save()

# 9. Eliminar una consulta veterinaria de prueba
consulta = ConsultaVeterinaria.objects.last()
consulta.delete()
```

La expresión `peso__gt=10` utiliza el lookup `gt`, que significa **greater than**, es decir, “mayor que”.

El doble guion bajo `__` separa el nombre del campo del lookup que Django debe aplicar. Este mismo mecanismo permite utilizar lookups como `icontains` para realizar búsquedas sin distinguir mayúsculas y minúsculas.

> Las operaciones de actualización y eliminación se muestran como ejemplos. Para repetirlas se recomienda utilizar registros creados específicamente para prueba.

---

## 16. Pruebas automatizadas

Ejecutar:

```powershell
python manage.py test
```

El proyecto contiene **6 pruebas automatizadas**:

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

La colección incluye **14 casos principales de prueba**:

1. GET para listar mascotas.
2. POST de una mascota válida.
3. POST de una mascota con peso `0`.
4. POST de una consulta válida.
5. GET de una mascota inexistente.
6. PATCH para actualizar una mascota.
7. GET de la página 2.
8. GET filtrando por especie.
9. POST de una consulta con costo negativo.
10. GET de perfil sin token.
11. GET de perfil con token válido.
12. GET de estadísticas con usuario regular.
13. GET de estadísticas con administrador.
14. DELETE de una mascota.

También se incluyen solicitudes auxiliares para obtener tokens de un usuario regular y de un administrador.

La colección utiliza marcadores como:

```text
Token TU_TOKEN_AQUI
```

y:

```text
TU_CONTRASENA_AQUI
```

para evitar almacenar credenciales reales.

> Para las pruebas PATCH y DELETE se debe sustituir el ID de la URL por el ID devuelto al crear la mascota de prueba.

---

## 18. Reflexiones

### Autenticación y autorización

La **autenticación** responde a la pregunta: **¿quién es el usuario?**

En este proyecto se utiliza `TokenAuthentication`. El usuario proporciona sus credenciales a `/api/token/` y recibe un token que posteriormente utiliza para identificarse ante la API.

La **autorización** responde a la pregunta: **¿qué puede hacer ese usuario?**

Esto puede observarse en los endpoints `/perfil/` y `/estadisticas/`.

`/perfil/` utiliza `IsAuthenticated`, por lo que cualquier usuario que se haya autenticado correctamente puede acceder.

`/estadisticas/` utiliza `IsAdminUser`. Por lo tanto, aunque un usuario regular tenga un token válido, no puede acceder a esa información porque no cuenta con permisos administrativos.

### Sesiones y HTTP

HTTP es un protocolo sin estado, por lo que cada solicitud es independiente y el servidor no recuerda automáticamente las solicitudes anteriores.

Django permite mantener información entre solicitudes mediante sesiones. El cliente conserva una identificación de sesión y Django utiliza esa identificación para recuperar los datos correspondientes.

Por esta razón, `/clinica/api/sesion/` puede mantener un contador de visitas para un mismo cliente aunque cada solicitud HTTP sea independiente.

### Organización de URLs

Las rutas específicas de la aplicación se encuentran en `clinica/urls.py`.

El archivo `veterinaria_backend/urls.py` se utiliza para incluir las rutas generales del proyecto, como el panel administrativo, las rutas de `clinica` y la obtención de tokens.

Esta separación mejora la organización del proyecto y permite mantener las rutas de cada aplicación de forma independiente.

---

## 19. Reflexión final: flujo para registrar una consulta veterinaria

Cuando Postman envía un POST, la solicitud llega a la **URL** `/clinica/api/consultas/`.
Django relaciona esa URL con la **View** encargada de registrar consultas.
La View recibe los datos y los envía al `ConsultaVeterinariaSerializer`.
El **Serializer** realiza la **validación** de los campos recibidos.
Si los datos son válidos, el Serializer utiliza el **Model** `ConsultaVeterinaria`.
Mediante el **ORM** de Django se crea el nuevo registro en la **base de datos**.
Una vez guardada la información, el Serializer transforma el objeto en datos JSON.
La View construye una **Response** con los datos serializados.
Finalmente, Django devuelve la Response a Postman con el código HTTP `201 Created`.

---

## 20. Git y GitHub

El desarrollo se realizó utilizando la rama:

```text
feature/sistema-veterinaria
```

El proyecto fue versionado con Git y publicado en GitHub.

Repositorio:

```text
https://github.com/salas-araya-444/sistema-gestion-veterinaria
```

La rama de desarrollo fue integrada a `main` mediante Pull Request.

---

## 21. Seguridad

El repositorio no incluye:

- Contraseñas reales.
- Tokens reales.
- Archivos `.env`.
- Entornos virtuales `.venv`.
- Carpetas `__pycache__`.
- Archivos `.pyc`.
- La base de datos local `db.sqlite3`.

Las migraciones de Django sí se encuentran versionadas.

---

## 22. Autor

**Esteban Salas Araya (C5J444)**
Universidad de Costa Rica, Sede del Pacífico
IF0009 - Desarrollo de Software IV
