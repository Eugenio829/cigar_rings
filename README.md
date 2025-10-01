# Proyecto Cigar Rings

Sistema de gestión para el control de producción de anillos de puros.

## Características

*(Describe aquí las principales características de tu aplicación. Por ejemplo:)*
- Gestión de inventario de materia prima (tintas, etc.).
- Registro y seguimiento de órdenes de producción de grabados.
- Control de almacén de productos terminados.
- Autenticación de usuarios y roles.

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo local.

### Prerrequisitos

- Python 3.10 o superior
- Git

### Pasos

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-DE-TU-REPOSITORIO>
    cd cigar_rings
    ```

2.  **Crea y activa un entorno virtual:**

    - En Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**

    Copia el archivo de ejemplo y edítalo con tus valores.
    ```bash
    copy .env.example .env
    ```
    Abre el archivo `.env` y reemplaza `your-secret-key-goes-here` con una clave secreta real de Django.

5.  **Aplica las migraciones de la base de datos:**
    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario:**

    He visto que tienes un comando personalizado para esto. ¡Buen trabajo!
    ```bash
    python manage.py create_custom_superuser
    ```

7.  **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

    La aplicación estará disponible en `http://127.0.0.1:8000/`.

---
*Este README fue generado por Gemini.*
