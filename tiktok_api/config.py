import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Config:
    PATH_TO_CHROME_DRIVER = str(os.getenv("PATH_TO_CHROME_DRIVER"))
    SCROLL_PAUSE = 1
    TMP_DIR = Path(os.getenv("TMP_DIR", default="../tmp_html/"))
    PATH_TO_VIDEO_DIR = Path(os.getenv("PATH_TO_VIDEO_DIR", default="../videos"))
