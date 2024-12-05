from __future__ import annotations

__all__ = ["WebAppData", "RAISE_EXCEPTIONS", "TGWPAQueryData"]

import hashlib
import hmac
import json
import logging
from datetime import datetime
from typing import Any, Dict, Literal
from urllib.parse import parse_qsl

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, computed_field, field_validator
from settings.manager import settings

RAISE_EXCEPTIONS = False

logger = logging.getLogger(__name__)


class WebAppDataChat(BaseModel):
    id: int
    type: Literal["group", "supergroup", "channel"]
    title: str
    username: str | None = None
    photo_url: str | None = None


class WebAppDataUser(BaseModel):
    id: int
    first_name: str

    is_bot: bool | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool = False
    allows_write_to_pm: bool = False
    photo_url: str | None = None


class WebAppData(BaseModel):
    _token: str = settings.TG_WEB_APP_BOT_TOKEN
    query_string: str
    _KEY: bytes = b"WebAppData"

    query_id: str | None = None
    user: WebAppDataUser | None = None
    receiver: WebAppDataUser | None = None
    chat: WebAppDataChat | None = None
    chat_type: Literal["sender", "private", "group", "supergroup", "channel"] | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None
    auth_date: datetime
    hash: str

    @classmethod
    def from_query_string(cls, query_string: str) -> WebAppData:
        data_ = cls._decode_string(query_string)
        data_["query_string"] = query_string
        for k, v in data_.items():
            if k in ["user", "receiver", "chat"]:
                data_[k] = json.loads(data_[k])
        return cls.model_validate(data_)

    @property
    def __secret_key(self) -> bytes:
        """Calculate the secret key"""
        return hmac.new(key=self._KEY, msg=self._token.encode("utf-8"), digestmod=hashlib.sha256).digest()

    @staticmethod
    def __json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def __str__(self) -> str:
        return json.dumps(
            self.model_dump(
                exclude_none=True,
                exclude_defaults=True,
                exclude={"_token", "_KEY", "query_string"},
            ),
            indent=2,
            default=self.__json_serializer,
        )

    def dict(self) -> Dict[str, Any]:  # noqa
        return self.model_dump(
            exclude_none=True,
            exclude_defaults=True,
            exclude={"_token", "_KEY", "query_string"},
        )

    @property
    def _data_check_string(self) -> str:
        data_ = self._decode_string(self.query_string)
        data_.pop("hash", "")
        data_check_arr = [f"{k}={v}" for k, v in sorted(data_.items())]
        return "\n".join(data_check_arr)

    def _calculate_hmac_hash(self) -> str:
        return hmac.new(
            key=self.__secret_key,
            msg=self._data_check_string.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    @property
    def is_valid(self) -> bool:
        if not hmac.compare_digest(self._calculate_hmac_hash(), self.hash):
            logger.warning(f"Invalid hash: \n{self}")
            return False
        logger.info(f"Data verified: \n{self.user.id}")
        return True

    def validate(self, *, raise_exception: bool = RAISE_EXCEPTIONS) -> None:
        if not self.is_valid:
            if raise_exception:
                raise ValueError(f"Invalid data: {self}")

    @staticmethod
    def _decode_string(data_: str) -> dict:
        return dict(parse_qsl(data_, keep_blank_values=True))


class TGWPAQueryData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    init_data: WebAppData | str

    @field_validator("init_data", mode="before")
    def parse_and_verify_init_data(cls, value: Any) -> Any:
        data = WebAppData.from_query_string(value)
        try:
            data.validate(raise_exception=True)
        except Exception as exc:
            msg = f'Invalid init data: \ndata_str: "{value}"\nobj: {data}'
            logger.error(msg)
            raise HTTPException(status_code=403, detail=f"Invalid init data: {exc}")
        return data

    @computed_field
    def user(self) -> WebAppDataUser:
        return WebAppDataUser.model_validate(self.init_data.user.model_dump(exclude_none=True, exclude_unset=True))
