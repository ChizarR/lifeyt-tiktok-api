from bs4 import BeautifulSoup


class Parser:
    """Parse html, using bs4 and lxml"""
    def __init__(self, parser: str="lxml") -> None:
        self._parser = parser

    def parse_links_from_account(self, html: str) -> list[str]:
        """Become source of account, then parse all links to video pages"""
        _class_name = "e1cg0wnj1"
        links = self.__get_links(html, _class_name)
        return links

    def parse_links_from_tag_page(self, html: str) -> list[str]:
        """Become source from tag page and returns all links from there"""
        _class_name = "e19c29qe7"
        links = self.__get_links(html, _class_name)
        return links

    def __get_links(self, html: str, class_name: str) -> list[str]:
        """Basic function to get list of links from account or tag pages"""
        soup = BeautifulSoup(html, self._parser)

        links = []
        video_cards = soup.find_all("div", class_=class_name)
        for card in video_cards:
            tag_a = card.find("a")
            href = tag_a.get("href")
            links.append(href)

        return links

    def parse_video_page(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")
        
        video_tag = soup.find_all("video")
        source_url = video_tag[0].get("src")

        reactions = soup.find_all("div", class_="ean6quk0")
        like_count = reactions[0].find(attrs={"data-e2e": "like-count"})
        comment_count = reactions[0].find(attrs={"data-e2e": "comment-count"})
        share_count = reactions[0].find(attrs={"data-e2e": "share-count"})
        
        return {
            "source-url": source_url,
            "like-count": like_count.text,
            "comment-count": comment_count.text,
            "share-count": share_count.text,
        }
        
