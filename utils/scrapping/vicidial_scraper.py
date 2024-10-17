from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common import exceptions as selexeptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pyautogui
import os
from django.conf import settings
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Literal
from pathlib import Path, WindowsPath


def login_keys():
    """
    Funcion para iniciar sesion automaticamente en la plataforma Vicidial
    """
    time.sleep(2.5)

    # Le pasamos las credenciales desde el archivo de configuracion usando .env
    pyautogui.write(settings.VICIDIAL_USER)
    pyautogui.press('tab')
    pyautogui.write(settings.VICIDIAL_PASSWORD)
    pyautogui.press('enter')

    time.sleep(1)


def get_vicidial_lists(
    driver: WebDriver,
    url: str,
    metodo: Literal['clean', 'download']
):
    """
    Obtiene los elementos de la tablas de la pestaña "listas" de la plataforma Vicidial

    :param driver: Una instancia de WebDriver para interactual con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param url: Link a plataforma vicidial (Trans/IVRs)
    :type url: str

    :param metodo: Accion que se realizará con las listas (clean/download)
    :type metodo: typing.Literal
    """

    try:
        # Obtenemos la URL
        driver.get(url)
        # Iniciamos sesión
        login_keys()
        time.sleep(2)
        # Obtenemos la pestaña de listas
        listas = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[8]/td/a'
        )))
        listas.click()
        time.sleep(2)
        # Obtenemos la tabla de listas
        tabla = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/center/table/tbody'
        )))
        # Obtenemos las filas
        rows = tabla.find_elements(By.TAG_NAME, 'tr')
        print('Obteniendo información...')
        if metodo == 'download':
            print('Descargando listas...')
        elif metodo == 'clean':
            print('Limpiando listas...')

        # Iteramos las filas para ejecutar la accion en cada fila
        for row in rows:
            try:
                # Obtenemos el link al registro
                link = row.find_element(By.XPATH, './td[1]')
                # Validamos los registros a entrar
                if link.text == 'LISTA ID':
                    continue
                else:
                    print(f'Lista ID ->{link.text}')
                    # Entramos al registro
                    link.click()
                    # Ejecutamos funcion para limpiar/descargar en base al parametro method
                    if metodo == 'clean':
                        contacts = get_contacts_charged(driver)
                        if contacts:
                            clean_lists(driver)
                    elif metodo == 'download':
                        contacts = get_contacts_charged(driver)
                        if contacts:
                            download_lists(driver)
                    time.sleep(1)
                    # Volvemos a la tabla de listas
                    driver.back()

            except (Exception) as err:
                print(f'Error -> {err}')

    except selexeptions.WebDriverException as err:
        print(f'Error -> {err}')


def get_contacts_charged(driver: WebDriver):
    """
    Obtiene los contactos marcables de un registro de lista Transaccional o IVR

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webriver.WebDriver
    """
    try:
        # Ubicamos el número de contactos cargados
        contactos = driver.find_element(
            By.XPATH, '//*[@id="vicidial_report"]/font/center[5]/table/tbody/tr[4]/td[2]/font')
        if contactos:
            print(f'Contactos cargados: {contactos.text}')
            return True
        else:
            raise selexeptions.NoSuchElementException()
    except selexeptions.NoSuchElementException as err:
        # Encontramos variante de XPATH para listas vacías
        contactos = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="vicidial_report"]/font/center[5]/table/tbody/tr[3]/td[2]/font'
        )))
        print(f'Contactos cargados: {contactos.text} \n')
        return False


def clean_lists(driver: WebDriver):
    """
    Limpia un registro de lista de IVR/Transaccinal si tiene contactos cargados

    :param driver: Una instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webriver.WebDriver
    """
    try:
        # Ubicamos el link para limpiar la lista
        clean_link = driver.find_element(
            By.XPATH, '//*[@id="vicidial_report"]/center/font/b/a[4]'
        )
        clean_link.click()
        clean_btn = driver.find_element(
            By.XPATH, '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/font/a'
        )
        # Limpiamos la lista
        if clean_btn:
            clean_btn.click()
            print('Limpiando...')
            comfirm_tag = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
                By.XPATH,
                '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/font/b'
            )))
            if comfirm_tag:
                driver.back()
                print(f'Lista limpiada con exito!\n')
            driver.back()

    except selexeptions.NoSuchElementException as err:
        print(f'Error -> {err}')


def download_lists(driver: WebDriver):
    """
    Descarga las listas que tienen rgistros

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webriver.WebDriver
    """

    try:
        download_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="vicidial_report"]/center/font/b/a[2]'
        )))
        download_link.click()
        print('OK...\n')
    except selexeptions.NoSuchElementException as err:
        print(f'Error -> {err}')


def upload_lists(
    driver: WebDriver,
    # link: str,
    file: WindowsPath
):
    """
    Carga los archivos de listas de IVRs y Transaccionales en la plataforma vicidial

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webriver.WebDriver

    :param link: Link a plataforma vicidial IVRs o Transaccionales
    :type link: str

    :param file: Referencia a archivo a cargar
    :type file: pathlib.WindowsPath
    """

    try:
        # Navegamos a link de cargue de listas
        upload_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[14]/td/a'
        )))
        upload_link.click()

        # RELLENAMOS PRIMER FORMULARIO
        # File input
        file_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input'
        )
        file_input.send_keys(os.path.abspath(file))

        # List override input
        list_override_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td[2]/font/select'
        )
        # Creamos una instancia de Select con el campo
        list_override_input = Select(list_override_input)
        # Iteramos las opciones para seleccionar la correspondiente
        for option in list_override_input.options:
            if file.stem in option.text:
                list_override_input.select_by_visible_text(option.text)
                print(f'Select input 1: {option.text}')
                break

        # Country code input (+57)
        country_code_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[3]/td[2]/font/select'
        )
        country_code_input = Select(country_code_input)
        country_code_input.select_by_visible_text('57 - COL')
        print('Country code selected: 57 - COL')

        # File type input
        file_type_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td[2]/font/input[2]'
        )
        # Clickeamos el radio imput si no esta seleccionado
        if not file_type_input.is_selected():
            file_type_input.click()
        print(f'File type input: Archivo personalizado')
        # Enviamos el formulario
        submit_btn_1 = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[12]/td/input[1]'
        )
        submit_btn_1.submit()
        print('FORMULARIO PARTE 1 -> OK...')

        # RELLENAMOS SEGUNDO FORMULARIO
        # vendor_lead_code_input
        vendor_lead_code_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((
            By.XPATH,
            '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[2]/td[2]/select'
        )))
        vendor_lead_code_input = Select(vendor_lead_code_input)
        vendor_lead_code_input.select_by_index(1)
        options = vendor_lead_code_input.options
        print(f'vendor_lead_code_input -> {options[1].text}')

        # source_id_input
        source_id_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[3]/td[2]/select'
        )
        source_id_input = Select(source_id_input)
        source_id_input.select_by_index(2)
        options = source_id_input.options
        print(f'source_id_input -> {options[2].text}')

        # phone_number_input
        phone_number_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td[2]/select'
        )
        phone_number_input = Select(phone_number_input)
        phone_number_input.select_by_index(3)
        options = phone_number_input.options
        print(f'phone_number_input -> {options[3].text}')

        # title_input
        title_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[5]/td[2]/select'
        )
        title_input = Select(title_input)
        title_input.select_by_index(4)
        options = title_input.options
        print(f'title_input -> {options[4].text}')

        # first_name_input
        first_name_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[6]/td[2]/select'
        )
        first_name_input = Select(first_name_input)
        first_name_input.select_by_index(5)
        options = first_name_input.options
        print(f'first_name_input -> {options[5].text}')

        # last_name_input
        last_name_input = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[8]/td[2]/select'
        )
        last_name_input = Select(last_name_input)
        last_name_input.select_by_index(7)
        options = last_name_input.options
        print(f'last_name_input -> {options[7].text}')

        # Obtenenos la etiqeta que contiene los inputs del segundo formulario
        tr_input_list = driver.find_element(
            By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[25]/th'
        )
        tr_input_list = tr_input_list.find_elements(By.TAG_NAME, 'input')
        submit_btn_2 = tr_input_list[0]

        # Enviamos el formulario
        # submit_btn_2 = driver.find_element(
        #     By.XPATH, '/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[25]/th/input[1]'
        # )
        submit_btn_2.click()

        print('FORMULARIO PARTE 2 --> OK')

        comfirm_tag = WebDriverWait(driver, 60).until(EC.presence_of_element_located((
            By.XPATH,
            '/html/body/table[2]/tbody/tr/td/center/font/b[2]'
        )))

        if comfirm_tag:
            lists_module = driver.find_element(
                By.XPATH, '/html/body/table[1]/tbody/tr/td[5]/a'
            )
            lists_module.click()
            print(f'{file.stem} cargado con exito!\n')
        else:
            raise selexeptions.NoSuchElementException(
                f'No se pudo confirmar el cargue de la lista {file.stem}'
            )

    except (selexeptions.WebDriverException, selexeptions.NoSuchElementException, selexeptions.TimeoutException) as err:
        print(f'Error -> {err}')


def get_campaigns(driver: WebDriver):
    login_keys()
    campaign_module = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        By.XPATH,
        '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[6]/td/a/font'
    )))
    campaign_module.click()

    tabla = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
        By.XPATH,
        '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[5]/td/table/tbody/tr/td/font/font/center/table/tbody'
    )))

    rows = tabla.find_elements(By.TAG_NAME, 'tr')
    return rows


def change_audio(
    driver: WebDriver,
    row: WebElement,
    items: dict,
    sleep: int = 2
):
    """
    Cambia un audio dentro de una campaña

    :param driver: Instancia de WebDriver para intercactuar con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param row: Fila de una tabla para interactuar con las columnas de esta
    :type row: selenium.webdriver.remote.webelement.WebElement

    :param items: Diccionario con nombre campaña: audio
    :type items: dict

    :param sleep: tiempo de espera
    :type sleep: int
    """

    try:
        # Nos dirigimos a vista detallada
        detailed_view = row.find_element(
            By.XPATH,
            './td[10]/font/a'
        )
        if detailed_view:
            detailed_view.click()
        time.sleep(sleep)

        # Identificamos nombre de campaña
        campaign_name_input = driver.find_element(
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[5]/td/table[2]/tbody/tr/td/font/center[1]/form/table/tbody/tr[2]/td[2]/input'
        )
        campaign_name = campaign_name_input.get_attribute('value')
        print(f'Cambiando audio a lista {campaign_name}.')

        # Obtenemos el nombre del audio a colocar segun el nombre de la campaña
        audio = ''
        for record in items:
            if campaign_name in record.values():
                audio = record['Nombre_Audio']

        print(f'Audio a colocar: {audio}')

        # Vamos a apartado encuesta
        poll = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[5]/td/table[1]/tbody/tr/td[8]/a/font'
        )))
        if poll:
            poll.click()
        time.sleep(sleep)

        # Cambiamos el audio
        audio_input = driver.find_element(
            By.XPATH,
            '//*[@id="survey_first_audio_file"]'
        )
        print(f'Audio anterior: {audio_input.get_attribute("value")}')
        if audio_input:
            audio_input.clear()
            audio_input.send_keys(audio)

        # Enviamos el fomrulario
        submit_button = driver.find_element(
            By.XPATH,
            '//*[@id="admin_form"]/center/table/tbody/tr[25]/td/input'
        )
        submit_button.click()
        print(f'Audio cambiado exitosamente!\n')

        time.sleep(sleep)

        # Volvemos a la lista de campañas
        driver.back()
        driver.back()
        driver.back()

    except selexeptions.NoSuchElementException as err:
        print(f'Error al intentar localizar elemento -> {err}')
    except selexeptions.TimeoutException as err:
        print(f'Tiempo de espera agotado\nError ->{err}')
