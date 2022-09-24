import os
from collections.abc import Iterator
from pathlib import Path


class FileManager:
    def __init__(self, tmp_dir: Path | None=None, 
                 video_dir: Path | None=None) -> None:
        self._current_dir = os.getcwd()

        if tmp_dir == None:
            self._tmp_dir = Path(self._current_dir, "tmp_files")
        else:
            self._tmp_dir = tmp_dir

        if video_dir == None:
            self._video_dir = Path(self._current_dir, "videos")
        else:
            self._video_dir = video_dir

    def write_file(self, data: str, file_name: str,
                   path: Path | None=None) -> Path:
        path = self._check_path(file_name, path)
        with open(path, "w", encoding="utf-8") as file:
            file.write(data)
        return path

    def read_file(self, path: Path) -> str:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
        return data

    def save_video(self, file_name: str, 
                   iter_content: Iterator, video_path: Path | None=None) -> Path:
        if video_path == None:
            os.makedirs(self._video_dir, exist_ok=True)
            path = Path(self._video_dir, file_name)
        else:
            os.makedirs(video_path, exist_ok=True)
            path = Path(video_path, file_name)

        with open(path, "wb") as file:
            for chunk in iter_content:
                if chunk:
                    file.write(chunk)
                    file.flush()
        return path

    def _check_path(self, file_name: str, path: Path | None) -> Path:
        """If path in args - returns path from args, else default path to tmp"""
        if path == None:
            os.makedirs(self._tmp_dir, exist_ok=True)
            return Path(self._tmp_dir, file_name)
        os.makedirs(self._tmp_dir, exist_ok=True)
        return Path(path, file_name)
        
