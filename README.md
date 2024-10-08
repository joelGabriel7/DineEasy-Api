# DineEasy API de Reservaciones de Restaurantes

## Descripción del Proyecto

DineEasy es una API robusta y escalable diseñada para automatizar el proceso de reservaciones en restaurantes. Desarrollada con Django Rest Framework (DRF), esta API proporciona una solución completa para la gestión de clientes, restaurantes y reservaciones, con características avanzadas como autenticación, paginación, operaciones CRUD, sistema de permisos y documentación automática.



## Características Principales

- **Gestión de Reservaciones**: 
  - Crear, leer, actualizar y eliminar reservaciones.
  - Listar todas las reservaciones.
  - Filtrar reservaciones por estado.
  - Obtener resumen de reservaciones por restaurante.

- **Gestión de Clientes**: 
  - Registro de nuevos clientes.
  - Obtener información del usuario actual.
  - Listar todos los usuarios y clientes.
  - Obtener resumen de reservaciones por cliente.

- **Gestión de Restaurantes**: 
  - Listar todos los restaurantes.
  - Obtener detalles de un restaurante específico.
  - Obtener resumen de reservaciones por restaurante.

- **Gestión de Mesas**:
  - Crear, leer, actualizar y eliminar mesas.
  - Listar todas las mesas.
  - Obtener mesas por restaurante.
  - Obtener resumen de mesas por restaurante.

- **Autenticación**: Sistema seguro de autenticación basado en tokens.

- **Autorización**: Control de acceso basado en roles y permisos.

- **Paginación**: Resultados paginados para una mejor experiencia de usuario y rendimiento.

- **Operaciones CRUD**: Soporte completo para operaciones Create, Read, Update y Delete en reservaciones, mesas y parcialmente en restaurantes y clientes.

- **Documentación Automática**: Integración con Swagger para una documentación de API interactiva y actualizada.

- **Base de Datos**: Soporta varios motores de bases de datos entre ellos PostgreSQL, MySQL y SQLite.



## Requisitos del Sistema

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- PostgreSQL 12+

## Uso de la API

La API estará disponible para acceder a la documentación interactiva de Swagger, visite `http://localhost:8000/api/docs/`.

## Endpoints Principales

### Restaurantes y Mesas

- `GET /api/restaurant/`: Lista todos los restaurantes
- `GET /api/restaurant/<int:pk>/`: Obtiene detalles de un restaurante específico
- `GET /api/restaurant/<int:restaurant_id>/reservation-summary/`: Resumen de reservaciones para un restaurante
- `GET /api/table/`: Lista todas las mesas y permite crear nuevas
- `GET /api/table/<int:pk>/restaurant/`: Obtiene mesas para un restaurante específico
- `GET /api/table/<int:restaurant_id>/table-summary/`: Resumen de mesas para un restaurante
- `GET, PUT, DELETE /api/table/<int:pk>/`: Operaciones CRUD para una mesa específica

### Clientes

- `POST /api/customer/register/`: Registra un nuevo cliente
- `GET /api/get/current/user`: Obtiene información del usuario actual
- `GET /api/users/`: Lista todos los usuarios
- `GET /api/users/customers/`: Lista todos los clientes
- `GET /api/users/customers/<int:customer_id>/customer-summary/`: Resumen de reservaciones para un cliente específico

### Reservaciones

- `GET, POST /api/reservations/`: Lista todas las reservaciones y permite crear nuevas
- `GET, PUT, DELETE /api/reservations/<int:pk>/`: Operaciones CRUD para una reservación específica
- `GET /api/reservations/status/`: Obtiene reservaciones filtradas por estado


## Instalación y Configuración

Siga estos pasos para configurar el proyecto en su entorno local:

1. **Clonar o Descargar el repositorio**:
   ```
   git clone [URL del repositorio]
   cd [nombre del directorio]
   ```

2. **Crear y activar un entorno virtual**:
   ```
   python -m venv venv
   source venv/bin/activate  
   # En Windows para activar `venv\Scripts\activate`
   ```

3. **Instalar las dependencias**:
   ```
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**:
   - Por defecto, el proyecto está configurado para usar SQLite. 
   - Si desea usar PostgreSQL o MySQL,
   - deberá modificar la configuración de la base de datos en `settings.py`.

5. **Crear y aplicar las migraciones**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear un superusuario** (opcional, pero recomendado para acceder al panel de administración):
   ```
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**:
   ```
   python manage.py runserver
   ```

La API ahora debería estar disponible en `http://localhost:8000/api/docs/`.

## Configuración Adicional (Próximamente)

En futuras actualizaciones, se proporcionarán instrucciones para:
- Configurar variables de entorno para mayor seguridad
- Ajustar la configuración para diferentes entornos (desarrollo, producción)
- Integrar servicios externos (si es aplicable)

