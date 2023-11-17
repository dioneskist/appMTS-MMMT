import datetime
import time
from dataclasses import dataclass

from elements.enum.hiterror import HitError


@dataclass
class Attempt:
    comparation: str
    key_comparation: str
    model: str
    key_model: str
    hit_or_error: HitError
    consecutive_hits: int
    latency_from_screen: datetime.datetime
