import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from .utils import Parser, parser_utils
from .utils.my_types import VideoInfo


BASE_URL = "https://www.tiktok.com/"


class TikTokRequester:
    """Create instance of webdriver, regulate requests to TikTok and form response data"""
    def __init__(self, path_to_chrome_driver) -> None:
        self._user_agent = UserAgent()
        self._options = self._set_default_options()
        self._driver = webdriver.Chrome(
            executable_path=path_to_chrome_driver,
            options=self._options
        )
        self._parser = Parser()

    def get_video_links_from_account(self, raw_account: str) -> list[str]:
        account = parser_utils.check_account_name(raw_account)
        url = BASE_URL + account
        self._driver.get(url)
        time.sleep(1)
        parser_utils.scroll_page(self._driver)
        html = self._driver.page_source
        links = self._parser.parse_links_from_account(html)
        return links

    def get_video_links_by_tag(self, tag: str) -> list[str]:
        url = BASE_URL + "tag/" + tag 
        self._driver.get(url)
        parser_utils.scroll_page(self._driver)
        html = self._driver.page_source
        links = self._parser.parse_links_from_tag_page(html)
        return links

    def download_video(self, link: str) -> VideoInfo:
        self._driver.get(link)
        time.sleep(1)
        html = self._driver.page_source
        video_info = self._parser.parse_video_page(html)
        video_id, account = parser_utils.parse_video_link(link)
        url = video_info["source-url"]
        path_to_saved_video = parser_utils.save_video(
            url, f"./videos/{account}/{video_id}.mp4"
        )
        return VideoInfo(
            account=account, 
            source_link=url,
            tiktok_link=link,
            like_count=video_info["like-count"],
            comment_count=video_info["comment-count"],
            share_count=video_info["share-count"],
            path_to_saved_video=path_to_saved_video
        )

    def _set_default_options(self) -> ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={self._user_agent.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        return options

