import time
import unittest
import builtins
from datetime import datetime, timedelta
from unittest.mock import mock_open, patch

from elements.attempt import Attempt
from elements.attemptlog import AttemptLog
from elements.enum.figura import Figura
from elements.enum.hiterror import HitError
from elements.resultlog import ResultLog
import pickle


class ResultLogTest(unittest.TestCase):
    participant = None
    date = datetime.now()
    start_time = None
    end_time = None
    result_log = ResultLog()

    attemptA1Equals: Attempt
    attemptA2NotEquals: Attempt

    deltatime_0_minute = timedelta(minutes=0)
    deltatime_1_minute = timedelta(minutes=1)
    deltatime_2_minute = timedelta(minutes=2)
    deltatime_5_minute = timedelta(minutes=5)

    def setUp(self):
        print('called')
        self.participant = 'teste 1'
        self.date = datetime.now()
        self.start_time = self.deltatime_0_minute
        self.end_time_5 = self.deltatime_5_minute
        self.test_type = 'TR AB/DE'

        self.attemptA1Equals = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                                       model=Figura.A1.value, key_model=Figura.A1.value[1], consecutive_hits=0,
                                       latency_from_screen=self.deltatime_1_minute, hit_or_error=HitError.HIT)
        self.attemptA2NotEquals = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                                          model=Figura.A2.value, key_model=Figura.A2.value[1], consecutive_hits=0,
                                          latency_from_screen=self.deltatime_2_minute, hit_or_error=HitError.ERROR)

    def test_creating_valid_result_log_filename_with_participant(self):
        self.result_log.participant = self.participant
        self.result_log.generate_filename()
        self.result_log.date = self.date

        expected_filename = 'teste1' + '_' + self.result_log.date.strftime(
            "%Y%M%d-%H%M%S") + '_' + self.result_log.test_type.replace(' ', '').replace('/', '') + '.bin'

        self.assertEqual(self.result_log.filename, expected_filename)

    def test_creatinbg_valid_result_log_filename_without_participant(self):
        self.result_log.generate_filename()

        expected_filename = 'unknown' + '_' + self.result_log.date.strftime(
            "%Y%M%d-%H%M%S") + '_' + self.result_log.test_type.replace(' ', '').replace('/', '') + '.bin'

        self.assertEqual(self.result_log.filename, expected_filename)

    def test_2_attempts_equals(self):
        result_log = self.result_log
        self.assertEqual(self.attemptA1Equals.comparation, self.attemptA1Equals.model)
        self.assertEqual(self.attemptA1Equals.key_comparation, self.attemptA1Equals.key_model)

    def test_2_attempts_equals_human(self):
        a1 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A1.value, key_model=Figura.A1.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_1_minute, hit_or_error=HitError.HIT)
        a1_csv = (
                    a1.comparation + "," + a1.key_comparation + "," + a1.model + "," + a1.key_model + "," +
                    a1.hit_or_error.HIT.value
                    + "," + str(a1.consecutive_hits) + "," + str(self.deltatime_1_minute))
        a2 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A2.value, key_model=Figura.A2.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_5_minute, hit_or_error=HitError.ERROR)
        a2_csv = (
                a2.comparation + "," + a2.key_comparation + "," + a2.model + "," + a2.key_model + "," +
                a2.hit_or_error.ERROR.value
                + "," + str(a2.consecutive_hits) + "," + str(self.deltatime_5_minute))
        self.assertEqual(a1_csv, ResultLog.attempt2csv(a1))
        self.assertEqual(a2_csv, ResultLog.attempt2csv(a2))

    def test_2_attempts_not_equals_and_total_errors(self):
        result_log = self.result_log

        self.assertNotEquals(self.attemptA2NotEquals.comparation, self.attemptA2NotEquals.model)
        self.assertNotEquals(self.attemptA2NotEquals.key_comparation, self.attemptA2NotEquals.key_model)

    def test_total_hits_errors_attempts(self):
        attempts = (self.attemptA1Equals, self.attemptA2NotEquals)

        total_attempts = AttemptLog.generate_attempts_total(attempts)
        total_hits = AttemptLog.generate_total_hits(attempts)
        total_errors = AttemptLog.generate_total_errors(attempts)

        self.assertEqual(total_attempts, 2)
        self.assertEqual(total_hits, 1)
        self.assertEqual(total_errors, 1)

    def test_validate_latency_total(self):
        a1 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A1.value, key_model=Figura.A1.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_1_minute, hit_or_error=HitError.HIT)
        a2 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A2.value, key_model=Figura.A2.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_5_minute, hit_or_error=HitError.ERROR)
        attempts = (a1, a2)
        latency_total = AttemptLog.generate_latency_total(attempts)
        latency_avg = AttemptLog.generate_latency_avg(attempts)
        self.assertEqual(latency_total, timedelta(minutes=6))
        self.assertEqual(latency_avg, timedelta(minutes=3))

    def test_adding_attemptsAB_and_attemptsDE(self):
        attempts_ab = list()
        attempts_ab.append(self.attemptA1Equals)
        attempts_de = list()
        attempts_de.append(self.attemptA1Equals)
        attempts_de.append(self.attemptA2NotEquals)

        self.result_log.attemptsAB = attempts_ab
        self.result_log.attemptsDE = attempts_de

        self.assertEqual(len(self.result_log.attemptsAB), 1)
        self.assertEqual(len(self.result_log.attemptsDE), 2)

    def test_open_file_mocked(self):
        with patch('builtins.open', mock_open(read_data='test')) as m:
            with open('foo') as f:
                content = f.read()
        m.assert_called_once_with('foo')
        assert content == 'test'

    def test_result_log_entire(self):
        result_log1 = ResultLog()
        result_log1.date = self.date
        result_log1.start_time = self.start_time
        result_log1.participant = self.participant
        result_log1.test_type = self.test_type
        result_log1.initialize_attempts()

        a1 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A1.value, key_model=Figura.A1.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_1_minute, hit_or_error=HitError.HIT)
        a2 = Attempt(comparation=Figura.A1.value, key_comparation=Figura.A1.value[1],
                     model=Figura.A2.value, key_model=Figura.A2.value[1], consecutive_hits=0,
                     latency_from_screen=self.deltatime_5_minute, hit_or_error=HitError.ERROR)
        # create mt
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a1)
        result_log1.attempts_mt.attempts.append(a2)
        result_log1.attempts_mt.attempts.append(a2)
        # create mm
        result_log1.attempts_mm.attempts.append(a1)
        result_log1.attempts_mm.attempts.append(a1)
        result_log1.attempts_mm.attempts.append(a2)
        result_log1.attempts_mm.attempts.append(a2)
        # create result_log
        result_log1.finalyze_resultlog()

        # assert result_log finalized
        self.assertEqual(result_log1.attempts_mt.latency_total, timedelta(minutes=16))
        self.assertEqual(result_log1.attempts_mm.latency_total, timedelta(minutes=12))
        self.assertEqual(result_log1.attempts_mt.latency_avg, timedelta(minutes=2))
        self.assertEqual(result_log1.attempts_mm.latency_avg, timedelta(minutes=3))
        self.assertEqual(result_log1.end_time, datetime.now())
        self.assertEqual(result_log1.date, self.date)
        self.assertEqual(result_log1.start_time, self.start_time)
        self.assertEqual(result_log1.attempts_mt.attempts_total, 8)
        self.assertEqual(result_log1.attempts_mm.attempts_total, 4)
        self.assertEqual(result_log1.attempts_mt.hits_total, 6)
        self.assertEqual(result_log1.attempts_mm.hits_total, 2)
        self.assertEqual(result_log1.attempts_mt.hits_errors, 2)
        self.assertEqual(result_log1.attempts_mm.hits_errors, 2)
        #
        # asserts reloaded from pickle
        result_log1_string = pickle.dumps(result_log1)
        result_log_loaded = pickle.loads(result_log1_string)
        self.assertEqual(result_log_loaded.participant, result_log1.participant)
        self.assertEqual(result_log_loaded.date, result_log1.date)
        self.assertEqual(result_log_loaded.start_time, result_log1.start_time)
        self.assertEqual(result_log_loaded.end_time, result_log1.end_time)
        self.assertEqual(result_log_loaded.test_type, result_log1.test_type)
        self.assertEqual(result_log_loaded.attempts_mt.latency_total, result_log1.attempts_mt.latency_total)
        self.assertEqual(result_log_loaded.attempts_mm.latency_total, result_log1.attempts_mm.latency_total)
        self.assertEqual(result_log_loaded.attempts_mt.latency_avg, result_log1.attempts_mt.latency_avg)
        self.assertEqual(result_log_loaded.attempts_mm.latency_avg, result_log1.attempts_mm.latency_avg)
        self.assertEqual(result_log_loaded.attempts_mt.attempts_total, 8)
        self.assertEqual(result_log_loaded.attempts_mm.attempts_total, 4)
        self.assertEqual(result_log_loaded.attempts_mt.hits_total, 6)
        self.assertEqual(result_log_loaded.attempts_mm.hits_total, 2)
        self.assertEqual(result_log_loaded.attempts_mt.hits_errors, 2)
        self.assertEqual(result_log_loaded.attempts_mm.hits_errors, 2)

        result_log1.generate_filename()
        # read file from pickle dump
        obj = pickle.dumps(result_log1)
        with patch('builtins.open', mock_open(read_data=obj)) as m:
            restored_obj = ResultLog.load_result_file(result_log1.filename)
            m.assert_called_once_with(result_log1.filename, 'rb')
            self.assertEqual(pickle.dumps(restored_obj), obj)

        # write file mocked
        content = pickle.dumps(result_log1)
        with patch('builtins.open', mock_open()) as m:
            ResultLog.write_result_file(result_log1)
            m.assert_called_once_with(result_log1.filename, 'wb')
            m().write.assert_called_once_with(content)

        csv_final = ''
        self.assertEqual(csv_final, ResultLog.generate_human_report(result_log1))

    def tearDown(self):
        print('teardown')
