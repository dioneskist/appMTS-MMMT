import datetime
import time
from dataclasses import dataclass

from elements.attempt import Attempt
from elements.enum.hiterror import HitError
from elements.modelMMMT import ModelMMMT

@dataclass
class AttemptLog:
    latency_total = time
    latency_avg = time
    hits_total = 0
    hits_errors = 0
    attempts_total = 0
    attempts_total_until_condition = 0

    attemptMM: ModelMMMT()
    attemptMT: ModelMMMT()

    @classmethod
    def generate_attempts_total(cls, attempts):
        return len(attempts)

    @classmethod
    def generate_total_hits(cls, attempts):
        count = 0
        for hit in attempts:
            if hit.hit_or_error == HitError.HIT.value:
                count += 1
        return count

    @classmethod
    def generate_total_errors(cls, attempts):
        count = 0
        for hit in attempts:
            if hit.hit_or_error == HitError.ERROR.value:
                count += 1
        return count

    @classmethod
    def generate_latency_total(cls, attempts):
        total = datetime.timedelta()
        for a in attempts:
            total += a.latency_from_screen
        return total

    @classmethod
    def generate_latency_avg(cls, attempts):
        total = datetime.timedelta()
        count = 0
        for a in attempts:
            total += a.latency_from_screen
        return total / len(attempts)

    @classmethod
    def generate_attempts_until_condition(cls, attempts):
        return 0
