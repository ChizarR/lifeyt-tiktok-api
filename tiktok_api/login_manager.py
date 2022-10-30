import time
from random import randint

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .config import Config


class LoginManager:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver 
        
    def test_auth(self, email, password):
        self._driver.get(Config.BASE_URL)        

        actions = ActionChains(self._driver)

        actions.pause(5)
        
        login_button = self._driver.find_element(By.CLASS_NAME, "ehk74z00")
        actions.pause(randint(2, 5))
        actions.move_to_element(login_button)
        actions.pause(randint(1, 3))
        actions.double_click(login_button).perform()

        actions.pause(randint(1, 10))

        login_via_email = self._driver.find_element(By.CLASS_NAME, "tiktok-r96wcy-DivBoxContainer")
        print(login_via_email)
        actions.move_to_element(login_via_email)
        actions.pause(randint(2, 4))
        actions.double_click(login_via_email).perform()

        actions.pause(randint(2, 6))

        login_via_email = self._driver.find_element(By.LINK_TEXT, "Log in with email or username")
        actions.move_to_element(login_via_email)
        actions.pause(randint(1, 3))
        actions.double_click(login_via_email).perform()

        name_field = self._driver.find_element(By.CLASS_NAME, "tiktok-11to27l-InputContainer")
        password_field = self._driver.find_element(By.CLASS_NAME, "tiktok-wv3bkt-InputContainer")
        
        actions.pause(randint(1, 3))

        actions.move_to_element(name_field)
        actions.click(name_field)
        for letter in email:
            actions.send_keys(letter)
            actions.pause(randint(1, 3) / 10)
        actions.perform()
        
        actions.move_to_element(password_field)
        actions.double_click(password_field)
        for letter in password:
            actions.send_keys(letter)
            actions.pause(randint(1, 3) / 10)
        actions.perform()
              
