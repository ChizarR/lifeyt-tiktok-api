import time
import logging
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from .config import Config
from .utils import FileManager, ParserUtils


logging.basicConfig(level=logging.INFO)


class TikTokParser:
    """The main tool for collecting data from TikTok"""

    BASE_URL = "https://www.tiktok.com/"
    path_to_driver = Config.PATH_TO_CHROME_DRIVER

    def __init__(self, tmp_dir: Path | None=None,
                 video_dir: Path | None=None) -> None:
        self._user_agent = UserAgent()
        self._options = self._set_default_options()
        self._driver = webdriver.Chrome(
            executable_path=Config.PATH_TO_CHROME_DRIVER,
            options=self._options
        )
        self._files = FileManager(tmp_dir, video_dir)
        self._utils = ParserUtils()

    def _set_default_options(self) -> ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={self._user_agent.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        return options

    def fetch_data_by_tag(self, tag: str):
        url = f"{TikTokParser.BASE_URL}tag/{tag}"
        logging.info(f"Sending request to {url}")
        self._driver.get(url)
        logging.info("Scrolling page...")
        self._utils.scroll_page(self._driver, Config.SCROLL_PAUSE)
        file_name = f"{tag}_index.html"
        html = self._driver.page_source
        path_to_tmp_file = self._files.write_file(html, file_name)
        logging.info("Parse links from page source...")
        video_links = self._get_video_links(path_to_tmp_file)
        logging.info("Get links page sources...")
        sources = self._get_sources_from_video_links(video_links)
        logging.info("Parsing video profiles...")
        video_info = self._parse_sources(sources)
        return video_info

    def _get_video_links(self, path_to_file: Path) -> list[str]:
        """Parse index html file to get links to videos"""
        links = []
        html = self._files.read_file(path_to_file)
        soup = BeautifulSoup(html, "lxml")
        video_cards = soup.find_all("div", class_="e19c29qe7")

        counter = 1
        for card in video_cards:
            logging.info(f"Parse link from card {counter}")
            raw_link = card.find("a")
            href = raw_link.get("href")
            links.append(href)
            counter += 1

        return links


    def fetch_data_by_account_name(self, account_name: str):
        account = self._check_account_name(account_name)
        url = f"{TikTokParser.BASE_URL}{account}"
        self._driver.get(url)
        self._utils.scroll_page(self._driver, Config.SCROLL_PAUSE)
        html = self._driver.page_source
        links = self._get_video_links_from_acc(html)
        paths_to_sources = self._get_sources_from_video_links(links)
        data = self._parse_sources(paths_to_sources)
        return data
        

    def _check_account_name(self, account_name: str) -> str:
        if account_name.startswith("@"):
            return account_name
        return f"@{account_name}"

    def _get_video_links_from_acc(self, html: str) -> list:
        clean_links = []
        soup = BeautifulSoup(html, "lxml")
        div_links = soup.find_all("div", class_="e1cg0wnj1")
        for index in range(0, len(div_links)):
            tag_a = div_links[index].find("a")
            href = tag_a.get("href")
            clean_links.append(href)
        return clean_links

    def _get_sources_from_video_links(self, video_links: list[str]) -> list[dict]:
        """Get source code from video pages"""
        paths_to_sources = []

        counter = 1
        for link in video_links:
            file_name, account = self._parse_link(link)
            logging.info(f"Getting source of link {counter}")
            self._driver.get(link)
            time.sleep(2) 
            html = self._driver.page_source
            path = self._files.write_file(html, file_name + ".html")
            paths_to_sources.append({
                "path_to_source_file": path,
                "file_name": file_name + ".mp4",
                "account": account
            })
            counter += 1

        return paths_to_sources

    def _parse_link(self, raw_link: str) -> tuple:
        """Take unique number from link to create unique filename"""
        link = raw_link.split("/")
        video_file_name = link[-1]
        account = link[-1]
        return (f"{video_file_name}", account) 

    def _parse_sources(self, video_info: list[dict]):
        """Get main info about video and save video"""
        counter = 1
        for video in video_info:
            logging.info(f"Parse video {counter}")
            try:
                html = self._files.read_file(video["path_to_source_file"])
                soup = BeautifulSoup(html, "lxml")
                video_tag = soup.find_all("video")
                print(video_tag)
                reactions = soup.find_all("div", class_="ean6quk0")
            
                video_url = video_tag[0].get("src")
                headers = {
                    "accept": "*/*",
                    "user-agent": self._user_agent.random
                }
                response = requests.get(video_url, headers=headers, stream=True)
                video_chunks = response.iter_content(chunk_size=1024)
                path_to_file = self._files.save_video(
                    video["file_name"], video_chunks
                )

                likes = reactions[0].find(attrs={"data-e2e": "like-count"})
                comments = reactions[0].find(attrs={"data-e2e": "comment-count"})
                shares = reactions[0].find(attrs={"data-e2e": "share-count"})
            except:
                logging.warning(f"Не вышло: {video['path_to_source_file']}")
                continue
            
            video["link_to_download_video"] = video_url
            video["path_to_downloaded_video"] = path_to_file
            video["likes"] = likes.text
            video["comments"] = comments.text
            video["shares"] = shares.text

            counter += 1
        return video_info
