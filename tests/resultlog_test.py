import time
import unittest
from datetime import datetime

from elements.attempt import Attempt
from elements.enum.figura import Figura
from elements.resultlog import ResultLog


class ResultLogTest(unittest.TestCase):
    participant = None
    start_time = None
    end_time = None
    result_log = ResultLog()

    def setUp(self):
        self.participant = 'teste 1'
        self.date = datetime.now()
        self.start_time = datetime.now()
        time.sleep(0.5)
        self.end_time = datetime.now()
        self.test_type = 'TR AB/DE'

    def test_create_valid_result_log_filename_with_participant(self):
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

    def test_create_valid_result_log_filename_without_participant(self):
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

        attempt1 = Attempt()
        attempt1.comparation = Figura.A1.name
        attempt1.key = Figura.A1.value
        attempt1.model = Figura.A1.name
        attempt1.key_model = Figura.A1.value
        self.assertEqual(attempt1.comparation, attempt1.model)
        self.assertEqual(attempt1.key, attempt1.key_model)

    def test_2_attempts_not_equals(self):
        result_log = self.result_log

        attempt1 = Attempt()
        attempt1.comparation = Figura.A1.name
        attempt1.key = Figura.A1.value
        attempt1.model = Figura.A2.name
        attempt1.key_model = Figura.A2.value
        self.assertNotEquals(attempt1.comparation, attempt1.model)
        self.assertNotEquals(attempt1.key, attempt1.key_model)

    def test_write_end_time(self):
        result_log = self.result_log
        result_log.generate_filename()
        result_log.create_result_file()
        result_log.end_time = datetime.now()
        result_log.write_end_time()
