import time

from selenium.webdriver.chrome.webdriver import WebDriver


class ParserUtils:
    def __init__(self) -> None:
        pass

    def scroll_page(self, driver: WebDriver, scroll_pause: int=2) -> None:
        """Scroll page to the last post, using js scripts"""
        prev_scroll_height = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            time.sleep(scroll_pause)
            curr_scroll_height = driver.execute_script(
                "return document.body.scrollHeight"
            ) 

            if curr_scroll_height == prev_scroll_height:
                break

            prev_scroll_height = curr_scroll_height
