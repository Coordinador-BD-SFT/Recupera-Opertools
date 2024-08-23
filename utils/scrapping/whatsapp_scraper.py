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


def get_driver():
    driver = None
    try:
        # Instalamos el driver
        service = ChromeService(ChromeDriverManager().install())
        # Iniciamos el driver
        driver = webdriver.Chrome(service=service)

        return driver
    except selexceptions.WebDriverException as err:
        print(f'Error -> {err}')


def quit_driver(driver):
    if driver is not None:
        driver.quit()


def get_whatsapp(driver, sleep=2):
    try:
        driver.get('https://web.whatsapp.com/')
        # iniciamos el driver
        wait = WebDriverWait(driver, 300)
        new_chat_btn = wait.until(EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
            )))
        new_chat_btn.click()
        time.sleep(sleep)

    except Exception as err:
        print(f'Error en get whatsapp -> {err}')


def search_num(driver, num, sleep=2):
    try:
        # Clickeamos el boton de nuevo chat y le enviamos el numero
        # new_chat_btn = driver.find_element(
        #     By.XPATH,
        #     '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        # )
        # new_chat_btn.click()
        text_box = driver.find_element(
            By.XPATH,
            '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p'
        )
        text_box.send_keys(num)
        time.sleep(sleep)

        # Validamos si numero es whatsapp
        try:
            chat = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME,
                    '_ak8q'
                ))
            )
            chat.click()
            return f'Fase 1 -> Encontrar numero: {num}\nCompletada con exito...', True

        except Exception:
            chat = False
            novedad = f'Fase 1 -> Encontrar numero: {num}\nFallido...\nFinalizando proceso...', False
            return chat, novedad

    except selexceptions.NoSuchElementException as err:
        print(f'Error en search num -> {err}')


def send_msj(driver, msj, sleep=2):
    try:
        text_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH,
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        )))
        text_box.click()
        text_box.clear()
        text_box.send_keys(msj)
        time.sleep(1)
        text_box.send_keys(Keys.ENTER)
        time.sleep(sleep)
        # send_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
        #     By.XPATH,
        #     '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
        # )))
        # send_btn.click()

        return f'Fase 2 -> Enviar mensaje: Finalizado con exito.\nContinuando...'

    except selexceptions.NoSuchElementException as err:
        print(f'Error en send mjs -> {err}')
