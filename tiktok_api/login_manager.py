import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver


class LoginManager:
    """Takes email and password"""

    LOGIN_URL = "https://www.tiktok.com/login"

    def __init__(self, email: str, password: str) -> None:
        self._password = password
        self._email = email

    def login(self, driver: WebDriver):
        driver.get(LoginManager.LOGIN_URL)
        # time.sleep(3)
        # driver.find_element(By.CLASS_NAME, "ehk74z00").click()
        time.sleep(4)
        driver.find_element(By.LINK_TEXT, "Use phone / email / username").click()
        time.sleep(4)
        driver.find_element(By.LINK_TEXT, "Log in with email or username").click()
        time.sleep(4)
        email_input = driver.find_element(By.CLASS_NAME, "etcs7ny1")
        password_input = driver.find_element(By.CLASS_NAME, "tiktok-wv3bkt-InputContainer")
        email_input.clear()
        email_input.send_keys(self._email)
        time.sleep(4)
        password_input.clear()
        password_input.send_keys(self._password)
        time.sleep(4)
        # password_input.send_keys(Keys.ENTER)
        driver.find_element(By.CLASS_NAME, "tiktok-cjigsp-Button-StyledButton").click()
        time.sleep(10)


    # def login(self, driver: WebDriver):
    #     email_input, password_input = self._get_login_form(driver)

    #     email_input.clear()
    #     email_input.send_keys(self._email)
    #     time.sleep(20)
    #     password_input.clear()
    #     password_input.send_keys(self._password)
    #     time.sleep(10)
    #     password_input.send_keys(Keys.ENTER)
    #     time.sleep(15)
    #     cookies = driver.get_cookies()
    #     return cookies


    # def _get_login_form(self, driver: WebDriver):
    #     driver.get(LoginManager.LOGIN_URL)
    #     email_input = driver.find_element(By.NAME, "username")
    #     password_input = driver.find_element(By.CLASS_NAME, "tiktok-wv3bkt-InputContainer")
    #     return (email_input, password_input)


