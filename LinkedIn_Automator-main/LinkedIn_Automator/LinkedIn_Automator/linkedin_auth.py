import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_and_login(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.linkedin.com/login")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
        time.sleep(5)
        if "feed" in driver.current_url:
            print("✅ Login Successful")
            return driver, wait
        else:
            print("❌ Login Failed")
            driver.quit()
            return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        driver.quit()
        return None, None    