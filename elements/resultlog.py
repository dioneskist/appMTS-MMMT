import csv
import logging
import pickle
import time
from datetime import datetime
from elements.attempt import Attempt
from elements.attemptlog import AttemptLog
import os

def attempts2csv(attempts):
    ret = ''
    for attempt in attempts:
        ret = ""
        ret += attempt.comparation + ","
        ret += attempt.key_comparation + ","
        ret += attempt.model + ","
        ret += attempt.key_model + ","
        ret += attempt.hit_or_error.value + ","
        ret += str(attempt.consecutive_hits) + ","
        ret += str(attempt.latency_from_screen)
        ret += '\n'
    return ret


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
    def write_result_file(cls, result_log_obj, folder):
        result_log_obj.generate_filename()
        final_folder = os.path.join(folder, result_log_obj.filename)
        with open(final_folder, 'wb') as f:
            f.write(pickle.dumps(result_log_obj))

    @classmethod
    def load_result_file(cls, filename):
        with open(filename, 'rb') as f:
            result_log_obj = pickle.load(f)
            return result_log_obj

    def finalyze_resultlog(self):
        if self.end_time is None:
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
    def generate_human_report(cls, result_log1):
        def add(s):
            return str(s) + '\n'
        res = add('')
        res += add('Participante: ' + str(result_log1.participant))
        res += add('Data: ' + str(result_log1.date))
        res += add('Hora de Início: ' + str(result_log1.start_time))
        res += add('Hora de conclusão: ' + str(result_log1.end_time))
        res += add('Treino/Teste: ' + result_log1.test_type)
        res += add('')
        res += add('Dados MM')
        res += add(ResultLog.attempts2csv(result_log1.attempts_mm.attempts, with_header=True))
        res += add('Latência Total: ' + str(AttemptLog.generate_latency_total(result_log1.attempts_mm.attempts)))
        res += add('Latência Média: ' + str(AttemptLog.generate_latency_avg(result_log1.attempts_mm.attempts)))
        res += add('Total de Acertos: ' + str(AttemptLog.generate_total_hits(result_log1.attempts_mm.attempts)))
        res += add('Total de Erros: ' + str(AttemptLog.generate_total_errors(result_log1.attempts_mm.attempts)))
        res += add('Total de pareamentos: ' + str(AttemptLog.generate_attempts_total(result_log1.attempts_mm.attempts)))
        res += add('Pareamentos até o critério: ' + str(AttemptLog.generate_attempts_until_condition(result_log1.attempts_mm.attempts)))
        res += add('')
        res += add('Dados MT')
        res += add(ResultLog.attempts2csv(result_log1.attempts_mt.attempts, with_header=True))
        res += add('Latência Total: ' + str(AttemptLog.generate_latency_total(result_log1.attempts_mt.attempts)))
        res += add('Latência Média: ' + str(AttemptLog.generate_latency_avg(result_log1.attempts_mt.attempts)))
        res += add('Total de Acertos: ' + str(AttemptLog.generate_total_hits(result_log1.attempts_mt.attempts)))
        res += add('Total de Erros: ' + str(AttemptLog.generate_total_errors(result_log1.attempts_mt.attempts)))
        res += add('Total de pareamentos: ' + str(AttemptLog.generate_attempts_total(result_log1.attempts_mt.attempts)))
        res += add('Pareamentos até o critério: ' + str(AttemptLog.generate_attempts_until_condition(result_log1.attempts_mt.attempts)))
        return res

    @classmethod
    def attempts2csv(cls, attempts, with_header=False):
        ret = ""
        if with_header:
            ret += 'COMPARAÇÃO,CHAVE COMPARAÇÃO,MODELO,CHAVE MODELO,A/E,ACERTO CONS.,LATÊNCIA\n'
        for attempt in attempts:
            ret += attempt.comparation + ","
            ret += attempt.key_comparation + ","
            ret += attempt.model + ","
            ret += attempt.key_model + ","
            ret += attempt.hit_or_error + ","
            ret += str(attempt.consecutive_hits) + ","
            ret += str(attempt.latency_from_screen)
            ret += '\n'
        return ret

    @classmethod
    def attempt2csv(cls, attempt):
        ret = ""
        ret += attempt.comparation + ","
        ret += attempt.key_comparation + ","
        ret += attempt.model + ","
        ret += attempt.key_model + ","
        ret += attempt.hit_or_error + ","
        ret += str(attempt.consecutive_hits) + ","
        ret += str(attempt.latency_from_screen)
        return ret
