import time
from pathlib import Path
from fake_useragent import UserAgent

import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from urllib3 import filepost

from .file_manager import FileManager


file_manager = FileManager() 


def scroll_page(driver: WebDriver, scroll_pause: int=2) -> None:
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


def check_account_name(account_name: str) -> str:
    if account_name.startswith("@"):
        return account_name
    return account_name


def parse_video_link(link: str) -> tuple[str, str]:
    splited_link = link.split("/")
    video_id = splited_link[-1]
    account = splited_link[-3]
    return video_id, account


def save_video(url: str, path_to_file: str) -> Path:
    splited_path = path_to_file.split("/")
    file_name = splited_path.pop()
    path = Path("/".join(splited_path))

    headers = {
        "accept": "*/*",
        "user-agent": UserAgent().random
    }

    response = requests.get(url, headers=headers, stream=True)
    video_chunks = response.iter_content(chunk_size=1024)
    fin_path = file_manager.save_video(file_name, video_chunks, path)
    return fin_path
    
