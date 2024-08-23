from enum import Enum
from pathlib import Path

from pydantic import AnyHttpUrl
from yt_dlp import YoutubeDL

from applications.youtube.models import YTVideoModel, YTChannelModel
from .console_logger import ConsoleLogger
from .exceptions import UrlUnknownHostError
from .progress_hooks import console_hook
from .structs import YTChannelInfo, YTPlaylistInfo, YTVideoInfo


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
    def source(self) -> UrlHostEnum:
        if self.__url.host in ["www.youtube.com", "www.youtu.be"]:
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
    _options: dict = None
    _info_raw: dict
    _info: YTVideoInfo | YTChannelInfo | YTPlaylistInfo

    def __init__(self, url: AnyHttpUrl | str, media_folder: Path, options: dict | None = None):
        """
        Initializes the MediaDownloader with the specified URL, media folder, and logger.

        Args:
            url (AnyHttpUrl): The URL to download media from.
            media_folder (Path): The folder to save the downloaded media.
        """
        self._url = Url(url)
        self._media_folder = media_folder
        self._client = YoutubeDL(self._get_yt_options())
        self._options = options
        if self._options and "outtmpl" not in self._options:
            self._options["outtmpl"] = f"{self._media_folder}/%(title)s.%(ext)s"

    @property
    def url(self) -> Url:
        return self._url

    def download(self):
        """
        Downloads media from the specified URL and saves it to the media folder.
        """

        self._client.download([self._url])

    def extract_info(self) -> YTVideoInfo | YTChannelInfo | YTPlaylistInfo:
        """
        Extracts information from the specified URL.
        """
        if self._url.source == UrlHostEnum.youtube:
            struct = None
            if self._url.is_video:
                struct = YTVideoInfo
                self.model = YTVideoModel
            elif self._url.is_channel:
                struct = YTChannelInfo
                self.model = YTChannelModel
            elif self._url.is_playlist:
                struct = YTPlaylistInfo
                self.model = YTPlaylist
            self._info_raw = self._client.extract_info(self._url, download=False)
            self._info = struct.model_validate(self._info_raw)
            return self._info

        raise UrlUnknownHostError(f"Unknown host: {self._url.source}")

    def _get_yt_options(self):
        """
        Returns the options for the YouTubeDL client.
        """
        if self._options:
            return self._options
        return {
            "format": "m4a/bestaudio/best",
            "logger": ConsoleLogger(),
            "progress_hooks": [console_hook],
            "outtmpl": f"{self._media_folder}/%(title)s.%(ext)s",
        }
