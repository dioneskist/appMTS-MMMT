import unittest

from elements.attempt import Attempt
from elements.resultlog import ResultLog


def test_validate_filename():
    reslog = ResultLog()
    reslog.generate_filename()
    print(reslog.filename)
    reslog.create_result_file()
    reslog.write_attempt(Attempt().__str__())


def test_attempt():
    attempt = Attempt()
    assert attempt.test_type == ""
