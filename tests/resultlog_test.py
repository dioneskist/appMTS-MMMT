import csv
import time
import unittest
import builtins
from datetime import datetime
from unittest.mock import mock_open, patch

from elements.attempt import Attempt
from elements.enum.figura import Figura
from elements.enum.hiterror import HitError
from elements.resultlog import ResultLog


class ResultLogTest(unittest.TestCase):
    participant = None
    start_time = None
    end_time = None
    result_log = ResultLog()

    attemptA1Equals: Attempt
    attemptA2NotEquals: Attempt

    def setUp(self):
        self.participant = 'teste 1'
        self.date = datetime.now()
        self.start_time = datetime.now()
        time.sleep(0.5)
        self.end_time = datetime.now()
        self.test_type = 'TR AB/DE'

        self.attemptA1Equals = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                                       model=Figura.A1.value, key_model=Figura.A1.value[1], consecutive_hits=0,
                                       latency_from_screen=datetime.now(), hit_or_error=HitError.HIT)
        self.attemptA2NotEquals = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                                          model=Figura.A2.value, key_model=Figura.A2.value[1], consecutive_hits=0,
                                          latency_from_screen=datetime.now(), hit_or_error=HitError.ERROR)

    def test_creating_valid_result_log_filename_with_participant(self):
        result_log = self.result_log
        result_log.participant = self.participant
        result_log.test_type = self.test_type
        result_log.date = self.date
        result_log.start_time = self.start_time
        result_log.end_time = self.end_time

        # MM_data = AttemptLog()
        # MT_data = AttemptLog()

        result_log.generate_filename()

        self.assertEqual(result_log.filename, 'teste1' + '_' + result_log.date.strftime(
            "%Y%M%d-%H%M%S") + '_' +
                         result_log.test_type.replace(' ', '').replace('/', '') + '.csv')

    def test_creatinbg_valid_result_log_filename_without_participant(self):
        result_log = self.result_log
        result_log.participant = ''
        result_log.test_type = self.test_type
        result_log.date = self.date
        result_log.start_time = self.start_time
        result_log.end_time = self.end_time

        # MM_data = AttemptLog()
        # MT_data = AttemptLog()

        result_log.generate_filename()

        self.assertEqual(result_log.filename, 'unknown' + '_' + result_log.date.strftime(
            "%Y%M%d-%H%M%S") + '_' +
                         result_log.test_type.replace(' ', '').replace('/', '') + '.csv')

    def test_2_attempts_equals(self):
        result_log = self.result_log

        self.assertEqual(self.attemptA1Equals.comparation, self.attemptA1Equals.model)
        self.assertEqual(self.attemptA1Equals.key_comparation, self.attemptA1Equals.key_model)

    def test_2_attempts_not_equals(self):
        result_log = self.result_log

        self.assertNotEquals(self.attemptA2NotEquals.comparation, self.attemptA2NotEquals.model)
        self.assertNotEquals(self.attemptA2NotEquals.key_comparation, self.attemptA2NotEquals.key_model)

    def test_write_end_time(self):
        result_log = self.result_log
        result_log.generate_filename()
        result_log.create_result_file()
        result_log.end_time = datetime.now()
        result_log.write_end_time()

    def test_adding_attemptsAB_and_attemptsDE(self):
        attempts_ab = list()
        attempts_ab.append(self.attemptA1Equals)
        attempts_ab.append(self.attemptA2NotEquals)
        attempts_de = list()
        attempts_de.append(self.attemptA1Equals)
        attempts_de.append(self.attemptA2NotEquals)

        self.result_log.attemptsAB = attempts_ab
        self.result_log.attemptsDE = attempts_de

        self.assertEqual(len(self.result_log.attemptsAB), 2)
        self.assertEqual(len(self.result_log.attemptsDE), 2)

    def test_open_file_mocked(self):
        with patch('builtins.open', mock_open(read_data='test')) as m:
            with open('foo') as f:
                content = f.read()
        m.assert_called_once_with('foo')
        assert content == 'test'
