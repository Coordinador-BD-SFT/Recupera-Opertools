import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def search(url):
    # chrome_options = Options()
    # chrome_options.add_argument()

    # Creamos el servicio instalando el driver
    service = ChromeService(ChromeDriverManager().install())

    # inicializamos el driver
    browser = webdriver.Chrome(service=service)

    # Relizamos la operacion especifica
    try:
        browser.implicitly_wait(10)
        browser.get(url)
        time.sleep(10)
    finally:
        browser.quit


# search('https://www.instagram.com')
