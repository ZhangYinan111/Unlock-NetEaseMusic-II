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
    browser.add_cookie({"name": "MUSIC_U", "value": "007E85C76BC77153C9F9DFA7946D0D1EF1A187B4F922A5598196D9F10DEC355FC074F31AB04DC7476E09AA2E23F6DB5DE307B19A354C960CEA7EFBC5AC6EC2D89934AE2D5490C607BAC0C2B8D5815C3BD0DE496EC386924038343017F20A235825942DFF2EDEA8C794EB1B93D1ECE45F7AFEC043B3050B861EE85C1D594E61DE32B0D052B9466EC3827145375169DCF0573204BF34E9849978C9A9231674E7A395BFF39E607B55B2DEDE1D00776B33A2F968800993B2649386736BD139FE617D47908AE3AAE86EEC925DD8C1DE3F5F015922933477C4CAF3376B621024589F0E5BC673B2C2725DE6450AF892E8BDA8083A7B5E67D740CEAECBAA1FD52C5A1B8890E59AA4BB86C020ABF3465018E72D64C52272C3EF5EFD76F0173E8196969AB4F9D2175F6E2A92848020483CC8413EC54DE3F762B8E1EDADF1846366C61CEFE3B7415D918CE4AC3D6246B48B0D3538CBF0BE2F64DD79C72404B2C2489EB9F97BD4
"})
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
