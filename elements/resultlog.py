import csv
import logging
import pickle
import time
from datetime import datetime
from elements.attempt import Attempt
from elements.attemptlog import AttemptLog


class ResultLog:
    """
    result log should write a file with content in format:
    """

    participant = ''
    date = datetime.now()
    start_time = datetime.now()
    end_time = None
    test_type = ""

    attempts_mt: AttemptLog
    attempts_mm: AttemptLog

    filename = ""
    extension = '.bin'

    def generate_filename(self):
        """
        filename = CANDIDATE_YYYYMMDD-DDHHMM_TESTTYPE
        i.e. = JOHN_20231018164821_TRABDE.bin

        :return:
        """

        test_type = self.test_type.replace(' ', '').replace('/', '')
        if self.participant == '':
            self.participant = 'unknown'
        filename = self.participant.replace(' ', '') + '_' + self.date.strftime(
            "%Y%M%d-%H%M%S") + '_' + test_type + self.extension
        self.filename = filename
        print("Generated filename: {}".format(self.filename))

    def create_result_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('Participante: ' + self.participant + '\n')
            f.write('Data: ' + self.date.strftime("%D") + '\n')
            f.write('Hora de Início: ' + self.start_time.strftime("%Y%M%d-%H%M%S") + '\n')
            f.write('END_TIME' + '\n')
            f.write('Treino/Teste: ' + self.test_type + '\n')

    def write_end_time(self):
        lines = ""
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if "END_TIME" in line:
                    line = 'Hora de Conclusão: ' + self.end_time.strftime("%Y%M%d-%H%M%S") + '\n'
                lines += line
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(lines)



    @classmethod
    def write_result_file(cls, result_log_obj):
        result_log_obj.generate_filename()
        with open(result_log_obj.filename, 'wb') as f:
            f.write(pickle.dumps(result_log_obj))

    @classmethod
    def load_result_file(cls, filename):
        with open(filename, 'rb') as f:
            result_log_obj = pickle.load(f)
            return result_log_obj

    def finalyze_resultlog(self):
        self.end_time = datetime.now()
        self.attempts_mt.hits_total = AttemptLog.generate_total_hits(self.attempts_mt.attempts)
        self.attempts_mt.hits_errors = AttemptLog.generate_total_errors(self.attempts_mt.attempts)
        self.attempts_mt.attempts_total = AttemptLog.generate_attempts_total(self.attempts_mt.attempts)
        self.attempts_mm.hits_total = AttemptLog.generate_total_hits(self.attempts_mm.attempts)
        self.attempts_mm.hits_errors = AttemptLog.generate_total_errors(self.attempts_mm.attempts)
        self.attempts_mm.attempts_total = AttemptLog.generate_attempts_total(self.attempts_mm.attempts)

        self.attempts_mt.latency_total = AttemptLog.generate_latency_total(self.attempts_mt.attempts)
        self.attempts_mm.latency_total = AttemptLog.generate_latency_total(self.attempts_mm.attempts)
        self.attempts_mt.latency_avg = AttemptLog.generate_latency_avg(self.attempts_mt.attempts)
        self.attempts_mm.latency_avg = AttemptLog.generate_latency_avg(self.attempts_mm.attempts)

    def validate_total_hits(self, total_hits):
        # compare whether total_hits is the same calculated by the resultlog
        total_hits_from_resultlog_calculator = AttemptLog.generate_total_hits(self.attempts_mt.attempts) +AttemptLog.generate_total_hits(self.attempts_mm.attempts)
        if total_hits == total_hits_from_resultlog_calculator:
            logging.debug('validate_total_hits: total hits calculated by main {} == calculated by resultlog {}'.format(
                total_hits, total_hits_from_resultlog_calculator))
        else:
            logging.debug(
                'validate_total_hits: ATTENTION total hits calculated by main {} != calculated by resultlog {}'.
                format(total_hits, total_hits_from_resultlog_calculator))
            return total_hits

    def initialize_attempts(self):
        self.attempts_mt = AttemptLog([])
        self.attempts_mm = AttemptLog([])

    @classmethod
    def attempt2csv(cls, attempt):
        ret = ""
        ret += attempt.comparation + ","
        ret += attempt.key_comparation + ","
        ret += attempt.model + ","
        ret += attempt.key_model + ","
        ret += attempt.hit_or_error.value + ","
        ret += str(attempt.consecutive_hits) + ","
        ret += str(attempt.latency_from_screen)
        return ret

    @classmethod
    def generate_human_report(cls, result_log1):
        return ''
