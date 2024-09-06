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


def get_whatsapp(driver, sleep=2):
    try:
        driver.get('https://web.whatsapp.com/')
        new_chat_btn = WebDriverWait(driver, 300).until(EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
            )))
        time.sleep(sleep)

    except selexceptions.NoSuchElementException as err:
        print(
            f'Error al intentar encontrar el elemento (get_whatsapp) -> {err}')
    except selexceptions.TimeoutException as err:
        print(f'Tiempo de espera agotado (get_whatsapp) -> {err}')


def new_chat_btn_exist():
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


def search_num(driver, num, sleep=2):
    try:
        # Buscamos y clickeamos boton de nevo chat
        new_chat_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        )))
        if new_chat_btn:
            time.sleep(1)
            new_chat_btn.click()

        # Buscamos y seleccionamos caja de texto y enviamos numeor a buscar
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

    except (selexceptions.NoSuchElementException, selexceptions.ElementClickInterceptedException):
        driver.refresh()
        return False


def send_msj(driver, msj, sleep=2):
    try:
        # Buscamos caja de texto
        time.sleep(sleep)
        text_box = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        )))
        if text_box:
            text_box.click()
            text_box.clear()
            text_box.send_keys(msj)
            time.sleep(1)
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
