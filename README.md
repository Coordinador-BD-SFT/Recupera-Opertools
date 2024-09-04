# Recupera-Opertools SAS

# Descripción
Este aplicativo consiste en un conjunto de funcionalidades que reducen el tiempo de ciertas actividades operativas, el cual fue construido
para automatizar y aligerar la carga a los coordinadores operativos.

## Características
- Reporte de whatsapp: Toma un extracto realizado por la extension WASUP de chrome, y lo cruza con las bases de envio de SMS .xlsx para generar reportes.
- Envío de whatsapp: Toma control de una ventana del navegador para realizar envios automáticos  en base a un archivo excel el cual debe contener
    las columnas Dato_Contacto y SMS.
- Administración de listas IVRs y transaccionales: (NO DISPONIBLE-Aún en desarrollo) Esta funcionalidad se encargara por sí sola de cargar, reiniciar, descargar y
    limpiar las listas transaccionales e IVRs que se manejan en la plataforma coroprativa VICIDIAL.

## Tecnologías y dependencias
Este proyecto utiliza pipenv para la gestión de las dependencias, en el archivo Pipfile y Pipfile.lock se encuentran todos los detalles sobre las
dependencias utilizadas.

## Instalación

1. **Instala ´pipenv´:**
    ```bash
    pip install pipenv

2. **Clona el repositorio y navega a la carpeta:**
    ```bash
    git clone https://github.com/Coordinador-BD-SFT/Recupera-Opertools
    
    cd Recupera-Opertools

3. **Instala las dependencias del Pipfile:**
    ```bash
    pipenv install

4. **Selecciona el interprete y activa el entorno:**
    Usa ´ctrl + shift + P´ en windows o ´cmd + shift + P´ en macOS/Linux, busca la opcion "Python: Select Interpreter"
    Luego ejecuta el siguiente comando
    ```bash
    pipenv shell

5. **Realiza las migraciones pendientes:**
    ```bash
    python manage.py migrate 

6. **Inicia el servidor y navega al servidor local que te brinda el aplicativo:**
    ```bash
    python manage.py runserver

    Puedes dar ´ctrl + clicl´/´cmd + click´ en el link que proporciona el comando o navegar directamente a él, se verá alco como esto:
    ´http://127.0.0.1:8000/´

Y listo! Ya puedes usar sin problemas el aplicativo

# Licencia
Este proyecto posee una licencia GNU General Public License v3.0, para más detalles puedes leer el archivo LICENSE