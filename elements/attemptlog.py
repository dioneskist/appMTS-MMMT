import time

from elements.attempt import Attempt


class AttemptLog:

    type_test = ""
    total_latency = time
    avg_latency = time
    hits_total = 0
    hist_errors = 0
    attempts_total = 0

    # attemps = list(Attempt)
