from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
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
            # clean_btn.click()
            print('Limpiando... \n')
            # time.sleep(1.8)
            driver.back()

    except selexeptions.NoSuchElementException as err:
        print(f'Error -> {err}')


def download_lists(driver: WebDriver):
    try:
        download_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="vicidial_report"]/center/font/b/a[2]'
        )))
        download_link.click()
        print('OK...\n')
    except selexeptions.NoSuchElementException as err:
        print(f'Error -> {err}')
