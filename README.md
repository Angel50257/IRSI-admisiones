Sistema de Gestión de Admisiones - IRSI 📌 

Descripción del Proyecto Este sistema permite gestionar de manera eficiente las solicitudes de admisión universitaria en distintos países de Centroamérica. El sistema centraliza los datos de los aplicantes, su historial de evaluaciones y los eventos relacionados con su proceso de admisión. Está diseñado para ser usado por distintos tipos de usuarios según su rol: administrador, asistente, director y consulta.

🛠️ Tecnologías Utilizadas Backend: Flask (Python)

Frontend: HTML5, Tailwind CSS, Bootstrap (según vista)

ORM: SQLAlchemy

Base de Datos: SQL Server

Autenticación: Flask-Login

Seguridad: Bcrypt para contraseñas, control de roles, validación de formularios

Exportación: Pandas + Openpyxl para generación de archivos Excel

✅ Requerimientos del Proyecto Requisitos Generales Python 3.10+

Base de datos SQL Server con procedimientos almacenados predefinidos

Paquetes Python:

bash Copy Edit pip install flask flask-login flask-wtf sqlalchemy pandas openpyxl bcrypt Configuración de entorno (archivo .env o variables) bash Copy Edit FLASK_APP=run.py FLASK_ENV=development 👥 Roles de Usuario y Funcionalidades

Administrador Acceso completo a todas las funciones del sistema
Gestión de usuarios (crear, editar, eliminar)

Registro y edición de aplicantes

Registro de historial por motivo o por evento (con trigger)

Edición del historial de un aplicante

Consulta global de aplicantes y eventos

Exportación de datos a Excel

Asistente Acceso completo como el administrador, pero con el rol “ASISTENTE”
Todas las funcionalidades administrativas, excepto gestión de otros usuarios

Acceso a vistas:

Aplicantes registrados

Registro de historial

Visualización de historial completo

Exportación de datos

Director Consulta de aplicantes registrados
Consulta de historial completo

Panel de acceso restringido sin opciones de edición

Exportación de datos

Consulta Solo puede visualizar los datos
No puede modificar información

Acceso limitado al panel de consulta de aplicantes y su historial

🔐 Seguridad Autenticación con Flask-Login

Hash de contraseñas con bcrypt

Roles definidos con decoradores @login_required y validación explícita

Separación de responsabilidades y control de vistas por rol

Protección contra CSRF y manipulación de formularios

📦 Estructura del Proyecto arduino Copy Edit IRSI-admisiones/ │ ├── app/ │ ├── models/ │ │ ├── usuario.py │ │ ├── aplicante.py │ │ └── historial.py │ ├── routes/ │ │ ├── aplicantes.py │ │ └── panel.py │ └── templates/ │ ├── panel_admin.html │ ├── panel_asistente.html │ ├── panel_director.html │ ├── panel_consulta.html │ ├── admin_aplicantes.html │ ├── admin_historial.html │ ├── admin_ver_todos_historial.html │ ├── admin_editar_historial.html │ └── otros templates según rol... │ ├── run.py └── README.md ▶️ Ejecución del Proyecto Configura la base de datos SQL Server y ejecuta los scripts de creación de tablas y procedimientos.

Crea el entorno virtual:

bash Copy Edit python -m venv .venv source .venv/bin/activate # En Linux/macOS .venv\Scripts\activate # En Windows Instala las dependencias:

bash Copy Edit pip install -r requirements.txt Inicia la aplicación:

bash Copy Edit flask run Accede en tu navegador a http://127.0.0.1:5000

📤 Exportación El administrador y asistente pueden exportar los datos de aplicantes a Excel mediante el botón Exportar a Excel.

📚 Procedimientos Requeridos en SQL Server InsertarAplicante

RegistrarHistorial

Trigger para insertar automáticamente en historial_eventos al modificar el estado de un aplicante

📌 Observaciones La gestión de observaciones del aplicante se realiza únicamente desde el historial.

Los eventos automáticos son gestionados por triggers definidos en la base de datos.

Se recomienda configurar roles en SQL Server para proteger los procedimientos de escritura.
