import sys
import os.path
import pickle
from elements.resultlog import ResultLog
import xlsxwriter


def write_excel_file(result_log, filename):

        filename = filename.replace('bin', 'xlsx')
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({"bold": True})
        datahora = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})
        deltatime = workbook.add_format({'num_format': 'hh:mm:ss.000'})

        worksheet.write('A1', 'Relatório de Pesquisa', bold)
        worksheet.write('A3', 'Participante')
        worksheet.write('B3', result_log.participant)
        worksheet.write('A4', 'Data')
        worksheet.write('B4', result_log.date, datahora)
        worksheet.write('A5', 'Hora de Início')
        worksheet.write('B5', result_log.start_time, datahora)
        worksheet.write('A6', 'Hora de conclusão')
        worksheet.write('B6', result_log.end_time, datahora)
        worksheet.write('A7', 'Treino/Teste')
        worksheet.write('B7', result_log.test_type)

        # dados MM
        worksheet.write('A10', 'Dados MM', bold)

        worksheet.write('A11', 'Comparação')
        worksheet.write('B11', 'Chave')
        worksheet.write('C11', 'Modelo')
        worksheet.write('D11', 'Chave Modelo')
        worksheet.write('E11', 'A/E')
        worksheet.write('F11', 'Acerto Consec.')
        worksheet.write('G11', 'Latência')

        row = 11
        for attempt in result_log.attempts_mm.attempts:
            worksheet.write(row, 0, attempt.comparation)
            worksheet.write_number(row, 1, int(attempt.key_comparation))
            worksheet.write(row, 2, attempt.model)
            worksheet.write_number(row, 3, int(attempt.key_model))
            worksheet.write(row, 4, attempt.hit_or_error)
            worksheet.write_number(row, 5, int(attempt.consecutive_hits))
            worksheet.write(row, 6, attempt.latency_from_screen, deltatime)
            row += 1

        row += 1
        worksheet.write(row, 0, 'Latência Total', bold)
        worksheet.write(row, 1, result_log.attempts_mm.latency_total, deltatime)
        row += 1
        worksheet.write(row, 0, 'Latência Média', bold)
        worksheet.write(row, 1, result_log.attempts_mm.latency_avg, deltatime)
        row += 1
        worksheet.write(row, 0, 'Total de Acertos', bold)
        worksheet.write_number(row, 1, result_log.attempts_mm.hits_total)
        row += 1
        worksheet.write(row, 0, 'Total de Erros', bold)
        worksheet.write_number(row, 1, result_log.attempts_mm.hits_errors)
        row += 1
        worksheet.write(row, 0, 'Total de Pareamentos', bold)
        worksheet.write_number(row, 1, result_log.attempts_mm.attempts_total)
        row += 1
        worksheet.write(row, 0, 'Total de Pareamentos ate o critério', bold)
        worksheet.write_number(row, 1, result_log.attempts_mm.attempts_total_until_condition)

        # dados MM
        row += 1
        worksheet.write(row, 0, 'Dados MT', bold)
        row += 1
        worksheet.write(row, 0, 'Comparação')
        worksheet.write(row, 1, 'Chave')
        worksheet.write(row, 2, 'Modelo')
        worksheet.write(row, 3, 'Chave Modelo')
        worksheet.write(row, 4, 'A/E')
        worksheet.write(row, 5, 'Acerto Consec.')
        worksheet.write(row, 6, 'Latência')
        row += 1
        for attempt in result_log.attempts_mt.attempts:
            worksheet.write(row, 0, attempt.comparation)
            worksheet.write_number(row, 1, int(attempt.key_comparation))
            worksheet.write(row, 2, attempt.model)
            worksheet.write_number(row, 3, int(attempt.key_model))
            worksheet.write(row, 4, attempt.hit_or_error)
            worksheet.write_number(row, 5, int(attempt.consecutive_hits))
            worksheet.write(row, 6, attempt.latency_from_screen, deltatime)
            row += 1
        row += 1
        worksheet.write(row, 0, 'Latência Total', bold)
        worksheet.write(row, 1, result_log.attempts_mt.latency_total, deltatime)
        row += 1
        worksheet.write(row, 0, 'Latência Média', bold)
        worksheet.write(row, 1, result_log.attempts_mt.latency_avg, deltatime)
        row += 1
        worksheet.write(row, 0, 'Total de Acertos', bold)
        worksheet.write_number(row, 1, result_log.attempts_mt.hits_total)
        row += 1
        worksheet.write(row, 0, 'Total de Erros', bold)
        worksheet.write_number(row, 1, result_log.attempts_mt.hits_errors)
        row += 1
        worksheet.write(row, 0, 'Total de Pareamentos', bold)
        worksheet.write_number(row, 1, result_log.attempts_mt.attempts_total)
        row += 1
        worksheet.write(row, 0, 'Total de Pareamentos ate o critério', bold)
        worksheet.write_number(row, 1, result_log.attempts_mt.attempts_total_until_condition)
        workbook.close()

def get_file(dropped):
	if not os.path.exists(dropped):
		print("Arquivo '" + dropped + "' inválido!")
		return None
	else:
		if os.path.isdir(dropped):
			print("Arquivo inválido!")
			return None
		else:
			filename = os.path.abspath(dropped)
			print("Processando '" + filename + "'!")
			with open(filename, 'rb') as file:
				return pickle.load(file), filename

			

def converter2excel(obj_content, filename):
	if obj_content is not None:
		result_log = obj_content
		print(ResultLog.generate_human_report(result_log))
		write_excel_file(result_log, filename)


args = sys.argv
if len(args) < 1:
	print("Arquivo não informado!")
	exit(1)
for arg in args[1:]:
	obj, filename = get_file(arg)
	converter2excel(obj, filename)
	
