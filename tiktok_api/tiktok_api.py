from .parser import TikTokParser


class TikTokApi:
    """Wrapper under TikTokParser"""
    def __init__(self) -> None:
        self._parser = TikTokParser()

    def get_videos_by_tag(self, tag: str) -> list[dict]:
        return self._parser.fetch_data_by_tag(tag)

    def get_account_info(self):
        pass

    def get_videos_from_account(self):
        pass
