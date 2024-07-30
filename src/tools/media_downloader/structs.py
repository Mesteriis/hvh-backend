from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, AnyHttpUrl


class DownloadItemStateStatusEnum(str, Enum):
    downloading = 'downloading'
    finished = 'finished'


class DownloadItemState(BaseModel):
    status: DownloadItemStateStatusEnum
    downloaded_bytes: int | dict | None = None
    total_bytes: int
    filename: str
    eta: int | dict | None = None
    speed: float | None = None
    elapsed: float | dict | None = None
    ctx_id: int | dict | None = None
    info_dict: dict
    eta_str: str | None = Field(None, alias='_eta_str')
    speed_str: str = Field(..., alias='_speed_str')
    percent_str: str = Field(..., alias='_percent_str')
    total_bytes_str: str = Field(..., alias='_total_bytes_str')
    total_bytes_estimate_str: str | None = Field(None, alias='_total_bytes_estimate_str')
    downloaded_bytes_str: str | None = Field(None, alias='_downloaded_bytes_str')
    elapsed_str: str = Field(..., alias='_elapsed_str')
    default_template: str = Field(..., alias='_default_template')

    def __str__(self):
        if self.status == DownloadItemStateStatusEnum.downloading:
            return self.default_template
        elif self.status == DownloadItemStateStatusEnum.finished:
            return f'{self.filename} has finished downloading.'


class YTVideoInfo(BaseModel):
    id: str
    title: str
    formats: list[dict]
    thumbnails: list[dict]
    thumbnail: AnyHttpUrl
    description: str
    channel_id: str
    channel_url: AnyHttpUrl
    duration: int
    view_count: int
    average_rating: float | None = None
    age_limit: int | None = None
    webpage_url: AnyHttpUrl
    categories: list[str]
    tags: list[str]
    playable_in_embed: bool
    live_status: str
    release_timestamp: int | None
    format_sort_fields: list[str] = Field(..., alias='_format_sort_fields')
    automatic_captions: dict
    subtitles: dict
    comment_count: int
    chapters: list[dict] | None
    heatmap: list[dict] | None = None
    like_count: int
    channel: str
    channel_follower_count: int
    channel_is_verified: bool | None = None
    uploader: str
    uploader_id: str
    uploader_url: AnyHttpUrl
    upload_date: str
    timestamp: int
    availability: str | None = None
    original_url: AnyHttpUrl
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    playlist: str | None
    playlist_index: int | None
    display_id: str
    fulltitle: str
    duration_string: str
    release_year: str | int | None
    is_live: bool
    was_live: bool
    requested_subtitles: str | None
    epoch: int
    asr: int
    filesize: int
    format_id: str
    format_note: str
    source_preference: int
    fps: int | None = None
    audio_channels: int
    height: int | None
    quality: float
    has_drm: bool
    tbr: float
    filesize_approx: int
    url: AnyHttpUrl
    width: int | None
    language: str | None = None
    language_preference: int
    preference: int | None = None
    ext: str
    vcodec: str
    acodec: str
    dynamic_range: str | None
    container: str
    downloader_options: dict
    protocol: str
    resolution: str
    aspect_ratio: str | None = None
    http_headers: dict
    audio_ext: str
    video_ext: str
    vbr: int
    abr: float
    format: str


class YTChannelInfo(BaseModel):
    id: str
    channel: str
    channel_id: str
    title: str
    availability: str | None = None
    channel_follower_count: int
    description: str
    tags: list[str]
    thumbnails: list[dict]
    uploader_id: str
    uploader_url: str
    modified_date: datetime | None
    view_count: int | None
    playlist_count: int | None
    uploader: str
    channel_url: AnyHttpUrl
    type: str = Field(..., alias='_type')
    entries: list[YTVideoInfo]
    extractor_key: str
    extractor: str
    webpage_url: str
    original_url: AnyHttpUrl
    webpage_url_basename: str
    webpage_url_domain: str
    release_year: str | None
    epoch: int


class YTPlaylistInfo(BaseModel):
    id: str
    title: str
    availability: str | None = None
    channel_follower_count: int | None
    description: str
    tags: list[str]
    thumbnails: list[dict]
    modified_date: str | None
    view_count: int | None
    playlist_count: int | None
    channel: str
    channel_id: str
    uploader_id: str
    uploader: str
    channel_url: AnyHttpUrl
    uploader_url: AnyHttpUrl
    type: str = Field(..., alias='_type')
    entries: list[YTVideoInfo]
    extractor_key: str
    extractor: str
    webpage_url: AnyHttpUrl
    original_url: AnyHttpUrl
    webpage_url_basename: str
    webpage_url_domain: str
    release_year: str | int | None = None
    epoch: int
