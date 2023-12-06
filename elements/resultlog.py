import csv
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

    attempts_ab = []
    attempts_de = []

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
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('Participante: ' + self.participant + '\n')
            f.write('Data: ' + self.date.strftime("%D") + '\n')
            f.write('Hora de Início: ' + self.start_time.strftime("%Y%M%d-%H%M%S") + '\n')
            f.write('END_TIME' + '\n')
            f.write('Treino/Teste: ' + self.test_type + '\n')

    def write_result_file(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write('Latência Total: ' + str(self.latency_total) + '\n')
            f.write('Latência Média: ' + str(self.latency_avg) + '\n')
            f.write('Total de acertos: ' + str(self.hits) + '\n')
            f.write('Total de erros: ' + str(self.errors) + '\n')
            f.write('Total de Pareamentos: ' + str(self.pareamentos_total) + '\n')
            f.write('Total de Pareamentos até o critério: ' + str(self.pareamentos_ate_acerto) + '\n')

    def write_attempts(self, attempts):
        with open(self.filename, 'a', encoding='utf-8') as f:
            for a in attempts:
                f.write(generate_csv(a) + '\n')

    def write_end_time(self):
        lines = ""
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if "END_TIME" in line:
                    line = 'Hora de Conclusão: ' + self.end_time.strftime("%Y%M%d-%H%M%S") + '\n'
                lines += line
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(lines)

    def write_excel_file(self):
        pass
        # filename = self.filename.replace('csv', 'xlsx')
        # workbook = xlsxwriter.Workbook(filename)
        # worksheet = workbook.add_worksheet()
        # bold = workbook.add_format({"bold": True})
        # datahora = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
        # deltatime = workbook.add_format({'num_format': 'hh:mm:ss.000'})
        #
        # worksheet.write('A1', 'Relatório de Pesquisa', bold)
        # worksheet.write('A3', 'Participante')
        # worksheet.write('B3', self.participant)
        # worksheet.write('A4', 'Data')
        # worksheet.write('B4', self.date, datahora)
        # worksheet.write('A5', 'Hora de Início')
        # worksheet.write('B5', self.start_time, datahora)
        # worksheet.write('A6', 'Hora de conclusão')
        # worksheet.write('B6', self.end_time, datahora)
        # worksheet.write('A7', 'Treino/Teste')
        # worksheet.write('B7', self.test_type)
        # worksheet.write('A9', 'Dados Teste')
        # worksheet.write('A10', 'Attemps')
        #
        # worksheet.write('A11', 'Comparação')
        # worksheet.write('B11', 'Chave')
        # worksheet.write('C11', 'Modelo')
        # worksheet.write('D11', 'Chave Modelo')
        # worksheet.write('E11', 'A/E')
        # worksheet.write('F11', 'Acerto Consec.')
        # worksheet.write('G11', 'Latência')
        #
        # row = 12
        # for attempt in self.attempts:
        #     worksheet.write(row, 0, attempt.comparation)
        #     worksheet.write_number(row, 1, int(attempt.key_comparation))
        #     worksheet.write(row, 2, attempt.model)
        #     worksheet.write_number(row, 3, int(attempt.key_model))
        #     worksheet.write(row, 4, attempt.hit_or_error)
        #     worksheet.write_number(row, 5, int(attempt.consecutive_hits))
        #     worksheet.write(row, 6, attempt.latency_from_screen, deltatime)
        #     row += 1
        #
        # row += 1
        # worksheet.write(row, 0, 'Latência Total', bold)
        # worksheet.write(row, 1, self.latency_total, deltatime)
        # row += 1
        # worksheet.write(row, 0, 'Latência Média', bold)
        # worksheet.write(row, 1, self.latency_avg, deltatime)
        # row += 1
        # worksheet.write(row, 0, 'Total de Acertos', bold)
        # worksheet.write_number(row, 1, self.hits)
        # row += 1
        # worksheet.write(row, 0, 'Total de Erros', bold)
        # worksheet.write_number(row, 1, self.errors)
        # row += 1
        # worksheet.write(row, 0, 'Total de Pareamentos', bold)
        # worksheet.write_number(row, 1, self.pareamentos_total)
        # row += 1
        # worksheet.write(row, 0, 'Total de Pareamentos ate o critério', bold)
        # worksheet.write_number(row, 1, self.pareamentos_ate_acerto)
        # workbook.close()


def attempt2csv(attempt):
    ret = ""
    ret += attempt.comparation + ","
    ret += attempt.key_comparation + ","
    ret += attempt.model + ","
    ret += attempt.key_model + ","
    ret += attempt.hit_or_error + ","
    ret += str(attempt.consecutive_hits) + ","
    ret += str(attempt.latency_from_screen)
    return ret


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
