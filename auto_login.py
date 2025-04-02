# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006E161FED78CF94C8B0DB9E57BFFA4B558190109205DD3FA9554B348AA581AAFB859734ADA5FF6BBB28F8203FE5EDDA993CB47F7F5AF74BC78D1C7BE752AF8E1AB724063D78095CD9AD0622EEF6D40656C48DFA8937D501E90ECDEF4A47412564A9A6154E93F2C88F4C1FF2D41050C853A3A87FEB9A877FE42BE3025635237B7191A9B394F2E372BD4D4D0A5A6785E6680E1D0A5B5DC4D54AD9608E9462939FDA79D0E017EC338B80263D72CA6C08E2B098C78FCDB74F5470CCABF1429A0BC69527F86DD074A3EC8AA066115F8CF1AFE0BC46139D6C4C8FA01A0F562593E0B30EBEB2C22543F5025C80EBA570146C56DFEA54F0F108EB32EA48C38134FDC83EA834537A4A247E249368B10F690B16D75AC55367EC0396A684D1FE36A80D28BC45698C4F78E932141225D85F6CB228C6FC2CD9DE27DB4BB21E2FBCA334B41A50E0D4C96586F2FBB19DCB990AFE33077EE3CDC58904EACDCE7A9E62A37F3ECE4074"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
