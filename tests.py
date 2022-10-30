import time
from pprint import pprint

from selenium import webdriver
from selenium_stealth import stealth

from tiktok_api import TikTokAPI
from tiktok_api.login_manager import LoginManager


tiktok_api = TikTokAPI("./drivers/chromedriver")


def test_fetch_links_by_account_name():
    account = "@sonyakisa8"
    return tiktok_api.fetch_account_links(account)


def test_fetch_links_by_tag():
    tag = "lions"
    return tiktok_api.fetch_tag_links(tag)


def test_download_video():
    link = "https://www.tiktok.com/@chipmunksoftiktok/video/6975140587196517638"
    problem_link = "https://www.tiktok.com/@sonyakisa8/video/6792126594891697414"
    return tiktok_api.get_video(problem_link)
    
    
def test_login_manager():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options, executable_path="./drivers/chromedriver")

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    login_manager = LoginManager(driver)
    email = "stanislav.konv27@gmail.com"
    password = "stStesTv2_327V"
    login_manager.test_auth(email, password)
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    print("-------- STARTED TEST --------\n")
    # print("[INFO] - 1. Fetch data from account '@chipmunksoftiktok'...\n")
    # pprint(test_fetch_links_by_account_name())
    # print("\n-------- CONTINUE TEST --------\n")

    # print("[INFO] - 2. Fetch data by tag 'lions'...\n")
    # pprint(test_fetch_links_by_tag())
    # print("\n-------- CONTINUE TEST --------\n")

    # print("[INFO] - 3. Dowloading video by link...\n")
    # pprint(test_download_video())

    print("[INFO] - 4. Login manager test...\n")
    pprint(test_login_manager())
    print("\n-------- END OF TEST --------\n")
