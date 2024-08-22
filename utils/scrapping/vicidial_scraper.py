import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def search(url):
    browser = None
    # Relizamos la operacion especifica
    try:
        # Creamos el servicio instalando el driver
        service = ChromeService(ChromeDriverManager().install())

        browser = webdriver.Chrome(service=service)
        # browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.get(url)
        time.sleep(10)
    except Exception as err:
        print(f'Ocurrio un error: {err}')
    finally:
        if browser is not None:
            browser.quit()

# search('https://www.instagram.com')
