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


def login_keys():
    """
    Funcion para iniciar sesion automaticamente en la plataforma Vicidial
    """
    time.sleep(3)

    # Le pasamos las credenciales desde el archivo de configuracion
    pyautogui.write(settings.VICIDIAL_USER)
    pyautogui.press('tab')
    pyautogui.write(settings.VICIDIAL_PASSWORD)
    pyautogui.press('enter')

    time.sleep(1)


def get_vicidial_IVRs(driver: WebDriver):
    """
    Obtiene los elementos de la lista de la pestaña "listas" de la plataforma Vicidial

    :param driver: Una instancia de WebDriver para interactual con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    """

    try:
        driver.get('https://192.227.124.58/vicidial/admin.php')
        login_keys()
        time.sleep(2)
        listas = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[8]/td/a'
        )))
        print('Modulo listas encontrado')
        listas.click()
        time.sleep(2)
        tabla = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '/html/body/center/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/font/center/table/tbody'
        )))
        rows = tabla.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                name_column = row.find_element(By.XPATH, './td[1]')
                name = name_column.find_element(By.TAG_NAME, 'a')
                print(name.get_attribute('href'))
                name.click()
                time.sleep(2)
                driver.back()
            except (selexeptions.NoSuchElementException, selexeptions.NoSuchAttributeException) as err:
                print(f'Error: {err}')

    except selexeptions.NoAlertPresentException as err:
        print(f'Error: {err}')
