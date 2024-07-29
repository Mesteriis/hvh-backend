from enum import Enum
from pathlib import Path

from pydantic import AnyHttpUrl
from yt_dlp import YoutubeDL

from .console_logger import ConsoleLogger
from .progress_hooks import console_hook


class UrlUnknownHostError(Exception):
    pass


class UrlHostEnum(str, Enum):
    youtube = "youtube"


class Url(str):
    __url: AnyHttpUrl

    def __init__(self, url: AnyHttpUrl | str):
        if isinstance(url, str):
            self.__url = AnyHttpUrl(url)
        else:
            self.__url = url

    @property
    def host(self) -> UrlHostEnum:
        if self.__url.host in ["youtube.com", "youtu.be"]:
            return UrlHostEnum.youtube
        else:
            raise UrlUnknownHostError(f"Unknown host: {self.__url.host}")

    @property
    def is_video(self) -> bool:
        return "watch" in self.__url.path

    @property
    def is_channel(self) -> bool:
        return "channel" in self.__url.path

    @property
    def is_playlist(self) -> bool:
        return "playlist" in self.__url.path

    def __str__(self):
        return str(self.__url)


class MediaDownloader:
    _url: Url
    _media_folder: Path
    _client: YoutubeDL

    def __init__(self, url: AnyHttpUrl | str, media_folder: Path):
        """
        Initializes the MediaDownloader with the specified URL, media folder, and logger.

        Args:
            url (AnyHttpUrl): The URL to download media from.
            media_folder (Path): The folder to save the downloaded media.
        """
        self._url = Url(url)
        self._media_folder = media_folder
        self._client = YoutubeDL(self._get_yt_options())

    def download(self):
        """
        Downloads media from the specified URL and saves it to the media folder.
        """

        self._client.download([self._url])

    def extract_info(self):
        """
        Extracts information from the specified URL.
        """
        c = self._client
        return c.extract_info(self._url, download=False)

    def _get_yt_options(self):
        """
        Returns the options for the YouTubeDL client.
        """
        return {
            'format': 'm4a/bestaudio/best',
            'logger': ConsoleLogger(),
            'progress_hooks': [console_hook],

            # # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            # 'postprocessors': [{  # Extract audio using ffmpeg
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'm4a',
            # }]
        }
