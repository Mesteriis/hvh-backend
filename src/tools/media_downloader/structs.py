from enum import Enum

from pydantic import BaseModel, Field


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
