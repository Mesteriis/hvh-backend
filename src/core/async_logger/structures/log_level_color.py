from pydantic import BaseModel


class LogLevelStringColor(BaseModel):
    """
    Модель, представляющая настройки цветов для уровней логирования в строковом формате.

    :param level_name: Название уровня логирования.
    :param fore: Цвет переднего плана для уровня логирования. По умолчанию используется None.
    :param back: Цвет заднего плана для уровня логирования. По умолчанию используется None.

    Класс Config в данной модели позволяет использовать произвольные типы данных (arbitrary_types_allowed = True).
    """

    level_name: str
    fore: str | None = None
    back: str | None = None

    class Config:
        arbitrary_types_allowed = True
