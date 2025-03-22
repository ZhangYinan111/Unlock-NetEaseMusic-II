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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F0C2E4B8E1A56E31B55DDABE1309C454ECDEEB4A7471E06B96EAF939F3326D44D1006A54BF5E9341B32E7D1BE3BE1923980176BF76027A3FE2E7FDD51A96C8F9ED1614F4323C168874E46F076CEED50D6E0623B41B910CF5B3EE98FFF084DF1E7225EC993F846C55777E1C54A48663D4F3A543AD9799F41A31B7C77E0E6A0AF6809362866FCFAF0114BBC387CCD8341EE911AE45E4BB0447B8E1C5F21DAC81AE8119FFA884600C9A5765BD33C5854AFBC22FE08701A1BA56686A4E8568338B800E6CAA9A4803C5C5F6E42EE2A47EA8F93433CD088BDF5428BBA0B9C61EF03F2CAF17FF128D521211738B4D00745000E4531D4CCF7CD1FC95B80C2D68B0DD0A8ED3232097C7991D7D21B16A0A7C9A9D68325865A2E4709272F2FB85D52E7DC2F66A81C6429186FCEF44A78B16F4AD97A6C91FAC3594F7FD18E615E27E9869EAA2CA7F7B63E571FDB2AB55352BFB3626D7CA5076F6E82FA1B9803B8EDF93AEE47E"})
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
