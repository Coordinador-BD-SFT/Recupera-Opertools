from django.core.files.storage import default_storage
from django.contrib.auth.models import AbstractUser
from utils.dataframes import whatsapp
from django.http import FileResponse
from django.utils import timezone
from django.db import models
from django.conf import settings
from pathlib import Path
from datetime import datetime
import pandas as pd
import os


# Create your models here.

# Modelo TipoReporte: Categoriza los tipos de reporte que maneja la app
class TipoReporte(models.Model):
    """
    Modelo encargado de ancapsular los reportes por categorias.

    parametros:
    name -> str: Nombre del tipo/categoria de reporte.
    created_at -> datetime: Fecha y hora de creación del objeto.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Función que retorna el campo nombre de la instancia en cuestión.
        """
        return self.name


# Modelo Reporte: Se encarga de crear los reportes cruzando los archivos .xlsx (mas adelante .csv y .json)
class Reporte(models.Model):
    """
    Modelo para crear y almacenar un reporte en base a un dataframe que contiene chats de whatsapp y cuentas
    asignadas con su repectiva campaña

    Parametros:
    campaign -> str|choices: Nombre de la  campaña con la que debe asociar los numeros del dataframe.
    chats_file -> file: Archivo que contiene los numeros que deben ser cruzados con las bases de datos de SMS.
    numero_inicio -> str: Numero inicial del intervalo que va a utilizar el cruce.
    numero_final -> str: Numero final(no incluido) del intervalo que va a utilizar el cruce.
    hora -> time: Hora selecionada por el usuario en la cual desea ver que se realizó el reporte. (Fines únicamente visuales)
    report_type -> Foreign Key: LLave foránea que categoriza el reporte con un tipo de reporte mediante su nombre.
    name -> str: Campo generado automaticamente con fines de nombrar el reporte y su archivo generado automaticamente.
    created_at -> datetime: Fecha y hora de creación del objeto.
    """
    campaigns_list = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
        ('multimarca', 'MULTIMARCA'),
    )
    campaign = models.CharField(max_length=15, choices=campaigns_list)
    chats_file = models.FileField(upload_to='files/upload/chats/')
    numero_inicio = models.CharField(max_length=11, blank=True)
    numero_final = models.CharField(max_length=11)
    hora = models.TimeField()
    report_type = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Función que retorna el nombre campo name del objeto
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        (DEPRECATED)
        Función que sobreescribe el metodo save de django.db.models.Model
        con el fin de crear el archivo del rpeorte al momento de crear una instancia
        del modelo.
        """

        # Obtenemos la fecha actual para uncluir en el nombre
        date = timezone.now().strftime('%Y-%m-%d')

        # Definimos el campo nombre de la instancia
        self.name = f'whatsapp-{self.campaign}-{date}-{self.hora}.xlsx'
        # Reemplazamos caracteres no aceptados para nombrar archivos
        self.name = self.name.replace(':', '-')

        # Ejecutamos el metodo crear_reporte de la instancia si es que
        # esta no se ha guardado aún evaluando si tiene o no pk (ID)
        if self.pk == None:
            self.crear_reporte()

        # Llamamos al metodo save() de django.db.models.Model para
        # guardar correctamente la instancia.
        super().save(*args, **kwargs)

    def crear_reporte(self):
        """
        Función para cruzar un dataframe que contiene números de whatsapp con una base de datos de SMS
        para crear un reporte personalizado
        """

        # Invocamos a data_base_filter para filtrar los que hicieron match.
        reporte = whatsapp.data_base_filter(
            # Seteamos el intervalo
            [self.numero_inicio, self.numero_final],
            # Referenciamos la base de SMS de la campaña asociada
            Path(f'files/upload/sms_databases/{self.campaign}/sms.csv'),
            # Archivo con numeros de whatsapp
            self.chats_file,
        )

        # Obtenemos el dataframe con los que hicieron match y la lista de los números no encontrados
        filtered_base, no_encontrado = reporte

        # Creamos dataframe con los registros de los NO encontrados
        lon = len(no_encontrado)
        marca = ['zNO EXISTE'] * lon
        cuenta = ['N/A'] * lon
        identificacion = ['N/A'] * lon

        numeros_append = pd.DataFrame({
            'Dato_Contacto': no_encontrado,
            'Edad_Mora': marca,
            'Cuenta_Next': cuenta,
            'Identificacion': identificacion,
        })

        # Concatenamos los dataframes
        file_no_encontrado = pd.concat(
            [filtered_base, numeros_append], ignore_index=True)
        # print(no_encontrado)

        # Creamos una ruta para el archivo que se va a servir
        path = Path(f'files/download/{self.name}')
        file_no_encontrado.drop_duplicates()
        final_file = file_no_encontrado.to_excel(path, index=False)
        # return FileResponse(open(path, 'rb'), as_attachment=True, filename=self.name)


def ruta_dinamica(instance, filename):
    """
    Función para dinamizar el guardado de un archivo en base a su nombre

    Parámetros:
    instance -> models.Model: Instancia de un modelo que contenga un campo name.
    """
    if not instance.pk:
        ext = instance.sms_base.path.split('.')[-1]
        return f'upload/sms_databases/{instance.name}/sms.{ext}'
    return filename


class SMSBase(models.Model):
    """
    Modelo encargado de administrar las bases de datos de envios SMS
    de las diferentes campañas

    Parámetros:
    tipo_reporte -> Foreign Key: Relaciona la instancia con un tipo de reporte con el fin de categorizar la base.
    name -> str|choices: Nombre asignado al modelo basado en campañas existentes.
    sms_base -> file: Archivo con registros de envio de SMS.
    created_at -> datetime: Fecha y hora de creación del objeto.
    """

    # QUITAR
    sms_type = (
        ('mora_30', 'MORA 30'),
        ('especiales', 'ESPECIALES'),
        ('castigo', 'CASTIGO'),
        ('multimarca', 'MULTIMARCA'),
    )
    # QUITAR

    tipo_reporte = models.ForeignKey(
        TipoReporte, on_delete=models.CASCADE, to_field='name')
    # Pasar a CharField común
    name = models.CharField(max_length=50, choices=sms_type)
    sms_base = models.FileField(upload_to=ruta_dinamica)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Función que retorna el campo name de la instancia
        """
        return self.name

    def limpiar_base(self):
        """
        Función que elimina las columnas innecesarias del archivo
        """
        base = pd.read_excel(self.sms_base, usecols=[
            'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'], dtype=str)

    def actualizar_base(self, nueva_base):
        """
        Función que agrega nuevos registros al campo sms_base de la instancia, descartando duplicados

        Parámetros:
        nueva_base -> file: Archivo con nuevos registros para la actualizar la base existente
        """

        try:
            print(f'Actualizando base {self.name}')
            # Creamos los dataframes de las bases nueva y antigua
            old_base = pd.read_csv(
                self.sms_base.path,
                usecols=[
                    'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'
                ],
                dtype=str,
                sep=',',
                encoding='utf-8'
            )
            new_base = pd.read_excel(nueva_base, usecols=[
                'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'], dtype=str)

            # Concatenamos la nueva base con la antigua
            df_unido = pd.concat([old_base, new_base], ignore_index=True)

            # Contamos duplicados para obtener informacion
            print(
                f'Se encontraron {df_unido.duplicated().sum()} registros repetidos.\nLimpiando...')

            # Limpiamos la base de los duplicados y la retornamos
            df_unido = df_unido.drop_duplicates(keep='last')
            df_unido.to_csv(
                self.sms_base.path,
                index=False,
                header=True,
                sep=',',
                encoding='utf-8'
            )

        except (ValueError, UnicodeEncodeError, UnicodeDecodeError) as err:
            print(f'Error al actualizar base\nError -> {err}')

    def save(self, *args, **kwargs):
        """
        Reescribimos el método save para que el campo sms_base sea limpiado antes de que
        se guarde la instancia
        """
        try:
            if self.sms_base:
                # Leemos la base segun su extension
                if '.xlsx' in self.sms_base.name:
                    print('Archivo excel')
                    base = pd.read_excel(
                        self.sms_base,
                        usecols=[
                            'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'
                        ],
                        dtype=str
                    )

                elif '.csv' in self.sms_base.name:
                    print('Archivo csv')
                    base = pd.read_csv(
                        self.sms_base,
                        usecols=[
                            'Identificacion', 'Cuenta_Next', 'Edad_Mora', 'Dato_Contacto'
                        ],
                        dtype=str
                    )

                # save_path = ruta_dinamica(self, self.sms_base.name)

                # os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # print(save_path)

                # Escribimos el archivo en la ruta designada
                base.to_csv(
                    f'media/upload/sms_databases/{self.name}/sms.csv',
                    index=False,
                    encoding='utf-8',

                )
                self.sms_base = f'upload/sms_databases/{self.name}/sms.csv'

            # Invocamos a save() del modelo padre para que se guarde correctamente la instancia
            super().save(*args, **kwargs)
        except Exception as err:
            print(f'Error al guardar el archivo de sms\nError -> {err}')
            print(self.sms_base.path)


class Usuario(AbstractUser):
    ranks = [
        ('trainee', 'TRAINEE'),
        ('junior', 'JUNIOR'),
        ('semisenior', 'SEMI SENIOR'),
        ('senior', 'SENIOR'),
    ]

    campaign = models.CharField(
        max_length=30, null=True,
        default='Sin Asignar'
    )
    points = models.IntegerField(default=0)
    rank = models.CharField(
        max_length=30, choices=ranks,
        null=True, default='Sin Asignar'
    )
    last_rank = models.CharField(max_length=30, choices=ranks)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='The groups this user belongs to',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        help_text='Specific permissions for this user',
        verbose_name='user permissions'
    )

    class Meta:
        permissions = [
            ('complete_access_to_reportes_app', 'Complete access to reportes app'),
            ('acces_to_customer_management', 'Access to customer management'),
        ]

    def __str__(self):
        return self.username

    def set_rank(self):
        pass

    @classmethod
    def update_points(cls):
        pass
