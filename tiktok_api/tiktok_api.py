from tiktok_api.utils.my_types import VideoInfo
from .requester import TikTokRequester


class TikTokApi:
    """Wrapper under TikTokRequester"""
    def __init__(self) -> None:
        self._requester = TikTokRequester()

    def fetch_account_links(self, account: str) -> list[str]:
        return self._requester.get_video_links_from_account(account)

    def fetch_tag_links(self, tag: str) -> list[str]:
        return self._requester.get_video_links_by_tag(tag)

    def get_video(self, video_link: str) -> VideoInfo:
        return self._requester.download_video(video_link)
