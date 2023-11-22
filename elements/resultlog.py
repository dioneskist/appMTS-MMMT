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
    latency_avg = None
    latency_total = None
    hits = 0
    errors = 0
    pareamentos_total = 0
    pareamentos_ate_acerto = 0

    attempts = []

    filename = ""
    extension = '.csv'

    def generate_filename(self):
        """
        filename = CANDIDATE_YYYYMMDD-DDHHMM_TESTTYPE
        i.e. = JOHN_20231018164821_TRABDE.csv

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
        with open(self.filename, 'w') as f:
            f.write('Participante: ' + self.participant + '\n')
            f.write('Data: ' + self.date.strftime("%D") + '\n')
            f.write('Hora de Início: ' + self.start_time.strftime("%Y%M%d-%H%M%S") + '\n')
            f.write('END_TIME' + '\n')
            f.write('Treino/Teste: ' + self.test_type + '\n')

    def write_result_file(self):
        with open(self.filename, 'a') as f:
            f.write('Latência Total: ' + str(self.latency_total) + '\n')
            f.write('Latência Média: ' + str(self.latency_avg) + '\n')
            f.write('Total de acertos: ' + str(self.hits) + '\n')
            f.write('Total de erros: ' + str(self.errors) + '\n')
            f.write('Total de Pareamentos: ' + str(self.pareamentos_total) + '\n')
            f.write('Total de Pareamentos até o critério: ' + str(self.pareamentos_ate_acerto) + '\n')

    def write_attempt(self, attempt):
        with open(self.filename, 'a') as f:
            f.write(generate_csv(attempt) + '\n')

    def write_end_time(self):
        lines = ""
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                if "END_TIME" in line:
                    line = 'Hora de Conclusão: ' + self.end_time.strftime("%Y%M%d-%H%M%S") + '\n'
                lines += line
        with open(self.filename, 'w') as f:
            f.write(lines)

    def write_excel_file(self):
        pass

def generate_csv(attempt):
    ret = ""
    ret += attempt.comparation + ","
    ret += attempt.key_comparation + ","
    ret += attempt.model + ","
    ret += attempt.key_model + ","
    ret += attempt.hit_or_error + ","
    ret += str(attempt.consecutive_hits) + ","
    ret += str(attempt.latency_from_screen)
    return ret
