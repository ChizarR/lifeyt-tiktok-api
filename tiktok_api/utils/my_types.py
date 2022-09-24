from pathlib import Path
from typing import NamedTuple


class VideoInfo(NamedTuple):
    account: str
    tiktok_link: str
    source_link: str
    like_count: int
    comment_count: int
    share_count: int 
    path_to_saved_video: Path
