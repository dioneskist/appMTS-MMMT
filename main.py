import logging
import os
import random
from datetime import datetime

from kivy.core.window import Window

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from elements.models import ScreenHandlerTT
from elements.resultlog import ResultLog
from telas.blanktela import BlankTela
from telas.instrucoes import TelaInstrucoes
from telas.menu import Menu
from telas.telatt import TelaTT
from telas.telatreinode import TelaTreinoDE
from telas.telatreinoab import TelaTreinoAB
from telas.telafinal import TelaFinal
from telas.participante import TelaNomeParticipante
from elements.elements import SourcePicture, TargetPicture, Imagem
from telas.telaVisualizar import TelaVisualizar
import itertools
import hashlib

width = 1200
height = 1920

Window.size = (width, height)
Window.clearcolor = (1, 1, 1, 1)


def get_de_ordem():
    lst = list()
    for i in range(6):
        ter = random.sample(range(1, 4), 3)
        for t in ter:
            lst.append(t)
    logging.debug('ordem gerada: {} ({})'.format(lst, len(lst)))
    return lst


def gerar_lista_usando_ordem_de(list_elementos, ordem):
    list_final = list()
    for o in ordem:
        logging.debug('validando {} {}'.format(o, len(list_elementos)))
        for item in list_elementos:
            if int(item[0][2]) == o:
                list_final.append(item)
                list_elementos.remove(item)
                break

    logging.debug('gerada lista final com ordem DE')
    for l in list_final:
        md5 = hashlib.md5(str(l).encode())
        logging.debug('{} {}'.format(l, md5.hexdigest()))
    return list_final


def gerar_todas_combinacoes(list1, list2, combinacoes_teste_DE=False):
    l1 = list(list1)
    l2 = list(list2)
    all_combinations = []
    counter = 0
    for x in l1:
        for y in l2:
            all_combinations.append(x + y)
            counter += 1
    logging.debug(
        'gerar_todas_combinacoes: gerada todas as combinacoes ({}) {}'.format(len(all_combinations), all_combinations))
    all_combinations_random = list()
    choices = random.sample(range(len(all_combinations)), len(all_combinations))
    for choice in choices:
        all_combinations_random.append(all_combinations[choice])
    logging.debug(
        'gerar_todas_combinacoes: gerada todas as combinacoes ({}) {}'.format(len(all_combinations_random),
                                                                              all_combinations_random))
    logging.debug('       combinacoes            ->      combinacoes aleatorias    ')
    index = 0
    for m in all_combinations:
        md5 = hashlib.md5(str(all_combinations_random[index]).encode())
        logging.debug('{} -> {}, {}'.format(all_combinations[index], all_combinations_random[index], md5.hexdigest()))
        index += 1

    if combinacoes_teste_DE:
        # ordena elementos de
        ordem_de = get_de_ordem()
        return gerar_lista_usando_ordem_de(all_combinations_random, ordem_de)
    else:
        return all_combinations_random


class GerenciadorDeTelas(ScreenManager):
    # flag para informar se a TelaTreinoAB foi respondida
    tela_treinoAB_finished = False
    tela_treinoDE_finished = False

    # flag para informar a tela atual
    tela_treinoAB_current = 0
    tela_treinoDE_current = 0
    all_combinacoes_XY = None
    all_combinacoes_ZW = None

    # flag para contar a quantidade de telas treinoDE respondidas após a tela treino
    tela_treinoDE_respondidas = 0

    """
        flag para contar quantas rodadas foram realizadas
        cada rodada eh uma sequencia de um treino + 3 testes
        em cada rodada sera necessario sortear novas figuras para os 3 testes
        seguindo a logica:
        teste 1 = figura 1 no target e alterar a ordem das sources
        teste 2 = figura 2 no target e alterar a ordem das sources
        teste 3 = figura 3 no target e alterar a ordem das sources
    """
    nr_rodada_teste = 0

    # contador global de acertos e erros
    acertos_total = 0
    acertos_total_str = StringProperty()
    erros_total = 0
    erros_total_str = StringProperty()
    total_acertos_necessarios = 0

    # ordem selecionada
    # pretreino ou ordem1 ou ordem2 ou ordemt
    ordem = StringProperty()

    # letras para os testes
    # virao sempre no padrao do teste, ex.:
    # 'TR AB/DE' (treino usam AB e testes usam DE)
    letters = StringProperty()

    # time
    tempo_maximo = 0.0
    time_inicio = None
    tempo_decorrido = None
    tempo_decorrido_str = StringProperty()

    latencia = None
    latencia_acerto_str = StringProperty()
    latencia_erro_str = StringProperty()

    start_screen_time = None

    # primeira tela
    primeira_tela = None

    # proxima
    proxima = ""

    # sabe previous screenmanager
    previouss_sm = None

    # total de telas validas para cada tipo
    total_telasAB_validas = 0
    total_telasDE_validas = 0

    # result log and repport
    result_log = None
    participant_name = None
    consecutive_hists = None



    def acertos_consecutivos(self):
        if self.consecutive_hists is None:
            self.consecutive_hists = 1
        else:
            self.consecutive_hists += 1

    def erros_consecutivos(self):
        self.consecutive_hists = 0

    def get_next_tela(self, next_expected):
        if next_expected == 'TelaTreinoAB':
            if self.tela_treinoAB_current >= self.total_telasAB_validas - 1:  # (0 a 35) >= 35
                return str(0)
            else:
                self.tela_treinoAB_current += 1
            return str(self.tela_treinoAB_current)
        if next_expected == 'TelaTreinoDE':
            if self.tela_treinoDE_respondidas == 0 and self.tela_treinoDE_current == 0:  # first screen
                return str(self.tela_treinoDE_current)
            else:
                if self.tela_treinoDE_current >= self.total_telasDE_validas - 1:  # (0 a 17) >= 17
                    self.tela_treinoDE_current = 0
                    return str(self.tela_treinoDE_current)
                else:
                    self.tela_treinoDE_current += 1
                    return str(self.tela_treinoDE_current)

    def comecar(self):
        """
        1 - Serao construidas as telas sob demanda para a ordem e letters escolhidas nas telas anteriores 2 - as
        telas serao geradas sob demanda com todas as combinacoes possiveis entre as letters 3 - as telas sao do tipo
        treinoAB e treinoDE quando escolhido 'TR AB/DE' e treinoBC e treinoEF quando escolhido 'TR BC/EF' 4 - as
        telas treinoAB usam o primeiro par de letras 5 - as telas treinoDE usam o segundo par de letras

        total_acertos_necessarios == ?, tempo_maximo == ?
        PT          - 12, 600
        TR AB       - 18, 1800
        TR BC       - 18, 1800
        TR MISTO    - 24, 1800

        :return:
        """
        logging.debug(
            'comecar: criando tela para ordem {} e letters {}'.format(self.ordem, self.letters))

        # if 'PT AB/DE' in self.letters:
        #     """
        #     for para criar as telas de treino com todas as combinacoes possiveis entre (x1,x2,x3 e y1,y2,y3)
        #     e (y1,y1,y3 e w1)
        #     tela treino usa as letras da posica 3 e 4 (AB) 'TR AB/DE'
        #     """
        #
        #     self.total_acertos_necessarios = 6
        #     self.tempo_maximo = 600.0
        #
        #     letter_x = str(self.letters[3]).lower()
        #     letter_y = str(self.letters[4]).lower()
        #     letter_z = str(self.letters[6]).lower()
        #     letter_w = str(self.letters[7]).lower()
        #     list_x = itertools.permutations([letter_x + '_1', letter_x + '_2', letter_x + '_3'], 3)
        #     list_y = itertools.permutations([letter_y + '_1', letter_y + '_2', letter_y + '_3'], 3)
        #     list_z = itertools.permutations([letter_z + '_1', letter_z + '_2', letter_z + '_3'], 1)
        #     list_w = itertools.permutations([letter_w + '_1', letter_w + '_2', letter_w + '_3'], 3)
        #     self.all_combinacoes_XY = gerar_todas_combinacoes(list_y, list_x, False)
        #     self.all_combinacoes_ZW = gerar_todas_combinacoes(list_z, list_w, combinacoes_teste_DE=True)
        #
        #     self.total_telasAB_validas = len(self.all_combinacoes_XY)
        #     self.total_telasDE_validas = len(self.all_combinacoes_ZW)
        #
        #     # cria primeira tela AB ou BC para comecar
        #     self.adiciona_tela(
        #         TelaTreinoAB(name='TelaTreinoAB_' + str(self.tela_treinoAB_current),
        #                      combinacoes=self.all_combinacoes_XY[self.tela_treinoAB_current],
        #                      ordem=self.ordem))
        #
        #     logging.debug('comecar: configurado telaAB_{} com combinacao={}'.format(self.tela_treinoAB_current,
        #                                                                             self.all_combinacoes_XY[
        #                                                                                 self.tela_treinoAB_current]))
        #     self.primeira_tela = 'TelaTreinoAB_' + str(self.tela_treinoAB_current)
        #
        # # valida se o é treino
        # if 'TR AB' in self.letters or 'TR BC' in self.letters:
        #     """
        #     for para criar as telas de treino com todas as combinacoes possiveis entre (x1,x2,x3 e y1,y2,y3)
        #     e (y1,y1,y3 e w1)
        #     tela treino usa as letras da posica 3 e 4 (AB) 'TR AB/DE'
        #     """
        #
        #     self.total_acertos_necessarios = 18
        #     self.tempo_maximo = 1800.0
        #
        #     letter_x = str(self.letters[3]).lower()
        #     letter_y = str(self.letters[4]).lower()
        #     letter_z = str(self.letters[6]).lower()
        #     letter_w = str(self.letters[7]).lower()
        #     list_x = itertools.permutations([letter_x + '_1', letter_x + '_2', letter_x + '_3'], 3)
        #     list_y = itertools.permutations([letter_y + '_1', letter_y + '_2', letter_y + '_3'], 3)
        #     list_z = itertools.permutations([letter_z + '_1', letter_z + '_2', letter_z + '_3'], 1)
        #     list_w = itertools.permutations([letter_w + '_1', letter_w + '_2', letter_w + '_3'], 3)
        #     self.all_combinacoes_XY = gerar_todas_combinacoes(list_y, list_x, False)
        #     self.all_combinacoes_ZW = gerar_todas_combinacoes(list_z, list_w, combinacoes_teste_DE=True)
        #
        #     self.total_telasAB_validas = len(self.all_combinacoes_XY)
        #     self.total_telasDE_validas = len(self.all_combinacoes_ZW)
        #
        #     # cria primeira tela AB ou BC para comecar
        #     self.adiciona_tela(
        #         TelaTreinoAB(name='TelaTreinoAB_' + str(self.tela_treinoAB_current),
        #                      combinacoes=self.all_combinacoes_XY[self.tela_treinoAB_current],
        #                      ordem=self.ordem))
        #
        #     logging.debug('comecar: configurado telaAB_{} com combinacao={}'.format(self.tela_treinoAB_current,
        #                                                                             self.all_combinacoes_XY[
        #                                                                                 self.tela_treinoAB_current]))
        #     self.primeira_tela = 'TelaTreinoAB_' + str(self.tela_treinoAB_current)
        #
        # # valida se o é misto
        # if 'TR Misto' in self.letters:
        #     self.total_acertos_necessarios = 24
        #     self.tempo_maximo = 600.0
        #     self.primeira_tela = 'TelaMisto_0'
        #     pass
        #     """
        #     for para criar as telas de treino com todas as combinacoes possibeis entre x1,x2,x3 e y1,y2,y3
        #     tela treino usa as letras da posica 3 e 4 'TR AB/DE'
        #     """
        #     letter_x = str(self.letters[3]).lower()
        #     letter_y = str(self.letters[4]).lower()
        #     list_x = itertools.permutations([letter_y + '_1', letter_y + '_2', letter_y + '_3'], 3)
        #     list_y = itertools.permutations([letter_x + '_1', letter_x + '_2', letter_x + '_3'], 3)
        #     all_combinacoes_XY = gerar_todas_combinacoes(list_x, list_y)
        #     index = 0
        #     for combinacao_xy in all_combinacoes_XY:
        #         self.adiciona_tela(TelaTreinoAB(name='telateste_' + str(index), combinacoes=combinacao_xy, ordem=self.ordem))
        #         index += 1
        #     self.current = 'TelaTreinoAB0'
        #     self.transition.direction = 'left'
        # if 'TT' in self.letters:
        #     self.previouss_sm = self
        #     self = ScreenHandlerTT()



    def iniciar_Time(self):
        self.time_inicio = Clock.get_time()
        logging.debug('iniciar_time: time iniciado ({})'.format(self.time_inicio))

    def tempo_decorrido_inicio(self):
        self.tempo_decorrido = Clock.get_time() - self.time_inicio
        self.tempo_decorrido_str = "Tempo decorrido do início: {0:.2f}".format(self.tempo_decorrido) + ' segundos'
        return self.tempo_decorrido

    def iniciar_treinos(self):
        if 'TT' in self.letters:
            print(self.letters)
            self.parent.change_sm()
        else:
            self.iniciar_Time()
            # self.gerar_resultlog_file()
            self.current = self.primeira_tela

    def gerar_resultlog_file(self):
        result_log = ResultLog()
        result_log.test_type = self.letters
        result_log.participant = self.participant_name
        result_log.generate_filename()
        result_log.create_result_file()
        self.result_log = result_log

    def write_attempt(self, attempt):
        self.result_log.attempts.append(attempt)
        self.result_log.write_attempt(attempt)

    def finalizar_result_file(self):
        self.result_log.end_time = datetime.now()
        self.result_log.write_end_time()

        self.result_log.hits = self.acertos_total
        self.result_log.errors = self.erros_total
        self.result_log.latency_total = datetime.now() - self.start_screen_time
        self.result_log.pareamentos_total = self.acertos_total + self.erros_total
        self.result_log.latency_avg = self.result_log.latency_total / self.result_log.pareamentos_total
        self.result_log.pareamentos_ate_acerto = 0
        self.result_log.write_result_file()
        self.result_log.write_excel_file()

    def troca_tela(self):

        """

        Sempre sera validada se o numero total de acertos foi atingido (18)
        se não foi atingido, sera validado se tela do treino ou teste
        esta completa, caso estejam seja recriada e a proxima tela sera chamada.
        Excessões:
            1 - Caso o os acertos forem igual aos acertos de cada tipo de treino ou teste, a tela final sera chamada
            2 - a tela teste sera sempre criada em numero de 3
                após o terceiro teste é que a tela treino volta a ser chamada

        First: validar TelaTreinoAB
        Second: validate telateste

        :param proxima_tela: nome da tela proxima tela
        :return:
        """

        tempo_decorrido = self.tempo_decorrido_inicio()
        logging.debug('Main.troca_tela: tempo decorrido entre acerto anterior e agora {}.'.format(tempo_decorrido))

        # valida final dos treinos e testes
        if self.acertos_total == self.total_acertos_necessarios or tempo_decorrido > self.tempo_maximo:
            tela_final = ''
            logging.debug('Main.troca_tela: total de acertos {}.'.format(self.acertos_total))
            logging.debug('Main.troca_tela: tela final sera chamada {}.'.format(tela_final))
            self.finalizar_result_file()
            self.acertos_total = 0
            self.acertos_total_str = str(self.acertos_total)
            self.erros_total = 0
            self.erros_total_str = str(self.erros_total)
            self.tela_teste_respondidas = 0
            self.add_widget(TelaFinal(name=tela_final))
            self.current = tela_final
        else:
            logging.debug('Main.troca_tela: total de acertos até o momento é {}.'.format(self.acertos_total))

            if self.tela_treinoAB_finished:
                self.tela_treinoAB_finished = False
                tela_atual = self.current
                proxima = 'TelaTreinoDE_' + self.get_next_tela('TelaTreinoDE')
                logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                self.adiciona_tela(
                    TelaTreinoDE(name=proxima,
                                 combinacoes=self.all_combinacoes_ZW[self.tela_treinoDE_current],
                                 ordem=self.ordem))
                self.ultima = self.current
                self.proxima = proxima

                # add blanktela and add schedule
                self.show_blanktela(1.5)

            if self.tela_treinoDE_finished:
                if self.tela_treinoDE_respondidas == 3:
                    self.tela_treinoDE_finished = False
                    self.tela_treinoDE_respondidas = 0
                    tela_atual = self.current
                    proxima = 'TelaTreinoAB_' + self.get_next_tela('TelaTreinoAB')
                    self.adiciona_tela(
                        TelaTreinoAB(name=proxima, combinacoes=self.all_combinacoes_XY[self.tela_treinoAB_current],
                                     ordem=self.ordem))
                    logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                    self.ultima = self.current

                    self.proxima = proxima

                    # add blanktela and add schedule
                    self.show_blanktela(0.5)
                else:
                    self.tela_treinoDE_finished = False
                    tela_atual = self.current
                    proxima = 'TelaTreinoDE_' + self.get_next_tela('TelaTreinoDE')
                    self.adiciona_tela(
                        TelaTreinoDE(name=proxima, combinacoes=self.all_combinacoes_ZW[self.tela_treinoDE_current],
                                     ordem=self.ordem))
                    logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                    self.ultima = self.current
                    self.proxima = proxima

                    # add blanktela and add schedule
                    self.show_blanktela(0.5)

    def show_blanktela(self, timeout):
        self.add_widget(BlankTela(name='blanktela'))
        self.current = 'blanktela'
        Clock.schedule_once(self.apagar_blanktela, timeout)

    def apagar_blanktela(self, delta_time):
        logging.debug('remove_tela: tela {} apagada'.format("blanktela"))
        Clock.unschedule(self.apagar_blanktela)
        self.current = self.proxima
        self.remove_tela(self.ultima)
        self.remove_widget(self.get_screen("blanktela"))

    def remove_tela(self, tela):
        try:
            self.remove_widget(self.get_screen(tela))
            logging.debug('remove_tela: tela {} apagada'.format(tela))
        except:
            logging.debug('remove_tela: tela {} não existe'.format(tela))

    def adiciona_tela(self, tela):
        try:
            # if not self.get_screen(tela):
            self.add_widget(tela)
            logging.debug('adiciona_tela: tela {} adicionada'.format(tela))
        except:
            logging.debug('adiciona_tela: tela {} não existe'.format(tela))

    def reiniciar_app(self):
        for screen in self.screen_names:
            if 'telatreinoAB' in screen:
                self.remove_tela(screen)
            if 'telatreinoDE' in screen:
                self.remove_tela(screen)
        self.current = 'menu'
        self.transition.direction = 'left'


class Main(App):
    title = 'TRTT'

    def start(self):
        kv_file = 'main.kv'
        self.load_kv(kv_file)

        sm = GerenciadorDeTelas()
        sh = ScreenHandlerTT()
        self.root = sh
        self.run()

    def change_sm(self):
        self.root = ScreenHandlerTT()
        self.run()


Main().start()
