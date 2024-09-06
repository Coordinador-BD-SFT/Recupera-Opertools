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


def get_vicidial_IVRs(driver):
    try:
        driver.get('https://192.227.124.58/vicidial/admin.php')

        driver.switch_to.alert.send_keys('recupera')
        time.sleep(5)

        common.quit_driver(driver)

        # listas = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((
        #     By.XPATH,
        #     '/html/body/center/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[8]/td/a'
        # )))
    except selexeptions.NoAlertPresentException as err:
        print(f'Error: {err}')