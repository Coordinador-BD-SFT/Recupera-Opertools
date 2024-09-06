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


def get_driver():
    driver = None
    try:
        # Instalamos el driver
        service = ChromeService(ChromeDriverManager().install())
        # Iniciamos el driver
        driver = webdriver.Chrome(service=service)

        # driver.switch_to.alert.send_keys()
        return driver
    except selexceptions.WebDriverException as err:
        print(f'Error -> {err}')


def quit_driver(driver):
    if driver is not None:
        driver.quit()
