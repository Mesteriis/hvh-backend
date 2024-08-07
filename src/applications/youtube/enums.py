from enum import Enum


class StatusEnum(Enum):
    new = "new"
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"