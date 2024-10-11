from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as selexceptions
from selenium.webdriver.chrome.webdriver import WebDriver
from random import randint


def get_whatsapp(
    driver: WebDriver,
    sleep: int = 2
):
    """
    Navega a whatsapp en una nueva instancia del navegador esperando hasta 5min a que se inicie sesion
    en ase a la búsqueda de un elemento

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param sleep: Define dinámicamente cuanto tiempo debe esperar el codigo para seguir ejecutandose
    :type sleep: int
    """
    try:
        # Navegamos a whatsapp web
        driver.get('https://web.whatsapp.com/')
        # Esperamos a que se inicie sesión con base a un elemento del dom
        new_chat_btn = WebDriverWait(driver, 300).until(EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
            )))
        time.sleep(sleep)

    except selexceptions.NoSuchElementException as err:
        print(f'Error al intentar encontrar el elemento -> {err}')
    except selexceptions.TimeoutException as err:
        print(f'Tiempo de espera agotado -> {err}')


def new_chat_btn_exist():
    """
    verifica si el boton de nuevo chat esta presente en el DOM
    """
    try:
        new_chat_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        )))
        if new_chat_btn:
            return new_chat_btn
        else:
            return False
    except Exception as err:
        print(f'Error en new chat click -> {err}')


def search_num(
    driver: WebDriver,
    num: str,
    sleep: int = 2
):
    """
    Busca un número telefonico en whatsapp y verifica si existe, caso contrario refresca el navegador

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param num: Numero telefonico a buscar en whatsapp
    :type num: str

    :param sleep: Define dinámicamente cuanto tiempo debe esperar el codigo para seguir ejecutandose
    :type sleep: int
    """
    try:
        # Buscamos y clickeamos boton de nevo chat
        new_chat_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        )))
        if new_chat_btn:
            time.sleep(randint(1, 5))
            new_chat_btn.click()

        # Buscamos y seleccionamos caja de texto y enviamos número a buscar
        text_box = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p'
        )))
        time.sleep(0.5)
        text_box.send_keys(num)
        time.sleep(1)

        # Validamos si numero es whatsapp
        chat_exist = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.CLASS_NAME,
            '_ak8q'
        )))

        if chat_exist:
            chat_exist.click()
            return True
        else:
            return False

    except (selexceptions.NoSuchElementException, selexceptions.ElementClickInterceptedException, selexceptions.TimeoutException) as err:
        print(f'Error: {err}')
        driver.refresh()
        return False


def send_msj(
    driver: WebDriver,
    msj: str,
    sleep: int = 2
):
    """
    Localiza la caja de texto del chat abierto y envia un mensaje

    :param driver: Instancia de WebDriver para interactuar con el navegador
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param msj:
    :type msj:

    :param sleep: Define dinámicamente cuanto tiempo debe esperar el codigo para seguir ejecutandose
    :type sleep: int
    """
    try:
        # Buscamos caja de texto
        time.sleep(sleep)
        text_box = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
        )))
        # Enviamos el mensaje
        if text_box:
            text_box.click()
            text_box.clear()
            text_box.send_keys(msj)
            time.sleep(randint(1, 10))
            text_box.send_keys(Keys.ENTER)
        else:
            print(f'No se encontro la caja de texto.\nReiniciando funcion...')
            time.sleep(sleep)
            send_msj(driver, msj)
        Keys.ESCAPE
        time.sleep(sleep)

    except selexceptions.NoSuchElementException as err:
        print(f'Error en send msj -> {err}')

    except selexceptions.StaleElementReferenceException as err:
        pass
