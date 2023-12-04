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

from elements.resultlog import ResultLog
from telas.blanktela import BlankTela
from telas.instrucoes import TelaInstrucoes
from telas.menu import Menu
from telas.telatestettab import TelaTesteTTAB
from telas.telatestettde import TelaTesteTTDE
from telas.telatt import TelaTT
from telas.telatreinode import TelaTreinoDE
from telas.telatreinoab import TelaTreinoAB
from telas.telafinal import TelaFinal
from telas.participante import TelaNomeParticipante
from elements.elements import SourcePicture, TargetPicture, Imagem
from telas.telaVisualizar import TelaVisualizar
import itertools
import hashlib

from utils.screen_combinations import preparar_combinacoes

width = 1200
height = 1920

Window.size = (width, height)
Window.clearcolor = (1, 1, 1, 1)


class GerenciadorDeTelas(ScreenManager):
    # flag para informar se a TelaTreinoAB foi respondida
    tela_AB_finished = False
    tela_DE_finished = False

    # flag para informar a tela atual
    tela_AB_current = 0
    tela_DE_current = 0
    all_combinacoes_XY = None
    all_combinacoes_ZW = None

    # SOMENTE MISTO
    isMisto = False
    tela_misto_AB_current = 0
    tela_misto_DE_current = 0

    """
    TREINO MISTO EH O USO DE DOIS TREINOS SIMULTANEAMENTE, TR AB/DE e TR BC/EF
    O TESTE EM EXECUCAO NA VEZ IRA SETAR O OUTRO TESTE COMO PROXIMO PARA QUE POSSA SER EXECUTADO
    EM ORDEM CORRETA:
    Ex.
    teste em execucao -> TR AB/DE -> entao o valor da variavel esta em current_treino_misto=BC/EF
    teste em execucao -> TR BC/EF -> entao o valor da variavel esta em current_treino_misto=AB/DE
    """
    current_treino_misto = ''

    # TELAS SOMENTE PARA MISTO
    all_combinacoes_XY_mistoAB = None
    all_combinacoes_XY_mistoBC = None
    all_combinacoes_ZW_mistoDE = None
    all_combinacoes_ZW_mistoEF = None

    # flag para contar a quantidade de telas treinoDE respondidas após a tela treino
    tela_DE_respondidas = 0

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
    total_hits_necessarios_saida = 0
    total_acertoserros_necessarios_saida = 0

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
    ultima = None

    # proxima
    proxima = ""
    screen_name_AB = ""
    screen_name_DE = ""

    # total de telas validas para cada tipo
    total_telasAB_validas = 0
    total_telasDE_validas = 0

    # SOMENTE PARA MISTO
    total_telas_mistoAB_validas = 0
    total_telas_mistoBC_validas = 0
    total_telas_mistoDE_validas = 0
    total_telas_mistoEF_validas = 0

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

    def get_next_tela(self, next_expected, is_misto):

        if next_expected in self.screen_name_AB:
            if is_misto:
                if self.current_treino_misto == 'AB':
                    if self.tela_misto_AB_current >= self.total_telas_mistoAB_validas - 1:  # (0 a 35) >= 35
                        self.tela_misto_AB_current = 0
                    else:
                        self.tela_misto_AB_current += 1
                    return str(self.tela_misto_AB_current)
                else:
                    if self.tela_misto_DE_current >= self.total_telas_mistoDE_validas - 1:  # (0 a 35) >= 35
                        self.tela_misto_DE_current = 0
                    else:
                        self.tela_misto_DE_current += 1
                    return str(self.tela_misto_DE_current)
            else:
                if self.tela_AB_current >= self.total_telasAB_validas - 1:  # (0 a 35) >= 35
                    self.tela_AB_current = 0
                else:
                    self.tela_AB_current += 1
                return str(self.tela_AB_current)
        elif next_expected in self.screen_name_DE:
            if is_misto:
                if self.tela_DE_respondidas == 0 and self.tela_misto_DE_current == 0:  # first screen
                    return str(0)
                else:
                    if self.tela_misto_DE_current >= self.total_telas_mistoDE_validas - 1:  # (0 a 17) >= 17
                        self.tela_misto_DE_current = 0
                    else:
                        self.tela_misto_DE_current += 1
                    return str(self.tela_misto_DE_current)
            else:
                if self.tela_DE_respondidas == 0 and self.tela_DE_current == 0:  # first screen
                    return str(0)
                else:
                    if self.tela_DE_current >= self.total_telasDE_validas - 1:  # (0 a 17) >= 17
                        self.tela_DE_current = 0
                    else:
                        self.tela_DE_current += 1
                    return str(self.tela_DE_current)

    def comecar(self):
        """
        1 - Serao construidas as telas sob demanda para a ordem e letters escolhidas nas telas anteriores 2 - as
        telas serao geradas sob demanda com todas as combinacoes possiveis entre as letters 3 - as telas sao do tipo
        treinoAB e treinoDE quando escolhido 'TR AB/DE' e treinoBC e treinoEF quando escolhido 'TR BC/EF' 4 - as
        telas treinoAB usam o primeiro par de letras 5 - as telas treinoDE usam o segundo par de letras

        total_acertoserros_necessarios_saida == ?, tempo_maximo == ?
        PT          - 12, 600
        TR AB       - 18, 1800
        TR BC       - 18, 1800
        TR MISTO    - 24, 1800

        :return:
        """
        logging.debug(
            'comecar: criando tela para ordem {} e letters {}'.format(self.ordem, self.letters))

        if 'PT AB/DE' in self.letters:
            """
            for para criar as telas de pre-treino com todas as combinacoes possiveis entre (x1,x2,x3 e y1,y2,y3)
            e (y1,y1,y3 e w1)
            tela treino usa as letras da posica 3 e 4 (AB) 'TR AB/DE'
            """

            self.total_hits_necessarios_saida = 12
            self.tempo_maximo = 600.0

            self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.letters)

            self.total_telasAB_validas = len(self.all_combinacoes_XY)
            self.total_telasDE_validas = len(self.all_combinacoes_ZW)
            self.screen_name_AB = 'TelaTreinoAB_'
            self.screen_name_DE = 'TelaTreinoDE_'

            # cria primeira tela AB ou BC para comecar
            self.adiciona_tela(
                TelaTreinoAB(name='TelaTreinoAB_' + str(self.tela_AB_current),
                             combinacoes=self.all_combinacoes_XY[self.tela_AB_current],
                             ordem=self.ordem))

            logging.debug('comecar: configurado telaAB_{} com combinacao={}'.format(self.tela_AB_current,
                                                                                    self.all_combinacoes_XY[
                                                                                        self.tela_AB_current]))
            self.primeira_tela = 'TelaTreinoAB_' + str(self.tela_AB_current)

        # valida se o é treino
        if 'TR AB' in self.letters or 'TR BC' in self.letters:
            """
            for para criar as telas de treino com todas as combinacoes possiveis entre (x1,x2,x3 e y1,y2,y3)
            e (y1,y1,y3 e w1)
            tela treino usa as letras da posica 3 e 4 (AB) 'TR AB/DE'
            """

            self.total_hits_necessarios_saida = 18
            self.tempo_maximo = 1800.0

            self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.letters)

            self.total_telasAB_validas = len(self.all_combinacoes_XY)
            self.total_telasDE_validas = len(self.all_combinacoes_ZW)
            self.screen_name_AB = 'TelaTreinoAB_'
            self.screen_name_DE = 'TelaTreinoDE_'

            # cria primeira tela AB ou BC para comecar
            self.adiciona_tela(
                TelaTreinoAB(name='TelaTreinoAB_' + str(self.tela_AB_current),
                             combinacoes=self.all_combinacoes_XY[self.tela_AB_current],
                             ordem=self.ordem))

            logging.debug('comecar: configurado telaAB_{} com combinacao={}'.format(self.tela_AB_current,
                                                                                    self.all_combinacoes_XY[
                                                                                        self.tela_AB_current]))
            self.primeira_tela = 'TelaTreinoAB_' + str(self.tela_AB_current)

        # valida se o é misto
        if 'TR Misto' in self.letters:
            """
            for para criar as telas de treino com todas as combinacoes possiveis entre (x1,x2,x3 e y1,y2,y3)
            e (y1,y1,y3 e w1)
            as telas usam as combinacoes dos testes TR AB/DE e TR BC/EF
            """

            self.total_hits_necessarios_saida = 12
            self.tempo_maximo = 1800.0

            # configure combinacoes for TR MISTO AB/DF
            self.all_combinacoes_XY_mistoAB, self.all_combinacoes_ZW_mistoDE = preparar_combinacoes('TR AB/DE')
            self.all_combinacoes_XY_mistoBC, self.all_combinacoes_ZW_mistoEF = preparar_combinacoes('TR BC/EF')

            self.total_telas_mistoAB_validas = len(self.all_combinacoes_XY_mistoAB)
            self.total_telas_mistoBC_validas = len(self.all_combinacoes_XY_mistoBC)
            self.total_telas_mistoDE_validas = len(self.all_combinacoes_ZW_mistoDE)
            self.total_telas_mistoEF_validas = len(self.all_combinacoes_ZW_mistoEF)
            self.screen_name_AB = 'TelaTreinoAB_'
            self.screen_name_DE = 'TelaTreinoDE_'
            self.isMisto = True
            self.current_treino_misto = 'AB'

            # configure combinacoes for TR MISTO AB/DF

            # cria primeira tela AB ou BC para comecar
            self.adiciona_tela(
                TelaTreinoAB(name='TelaTreinoAB_' + str(self.tela_misto_AB_current),
                             combinacoes=self.all_combinacoes_XY_mistoAB[self.tela_misto_AB_current],
                             ordem=self.ordem))

            logging.debug('comecar: configurado tela_mistoAB_{} com combinacao={}'.format(self.tela_misto_AB_current,
                                                                                          self.all_combinacoes_XY_mistoAB[
                                                                                              self.tela_misto_AB_current]))
            self.primeira_tela = 'TelaTreinoAB_' + str(self.tela_misto_AB_current)

        if 'TT' in self.letters:
            self.total_hits_necessarios_saida = 18
            self.tempo_maximo = 600.0

            self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.letters)

            self.total_telasAB_validas = len(self.all_combinacoes_XY)
            self.total_telasDE_validas = len(self.all_combinacoes_ZW)
            self.screen_name_AB = 'TelaTesteTTAB_'
            self.screen_name_DE = 'TelaTesteTTDE_'

            # cria primeira tela AB ou BC para comecar
            self.adiciona_tela(
                TelaTesteTTAB(name=self.screen_name_AB + str(self.tela_AB_current),
                              combinacoes=self.all_combinacoes_XY[self.tela_AB_current],
                              ordem=self.ordem))

            logging.debug('comecar: configurado telaAB_{} com combinacao={}'.format(self.tela_AB_current,
                                                                                    self.all_combinacoes_XY[
                                                                                        self.tela_AB_current]))
            self.primeira_tela = self.screen_name_AB + str(self.tela_AB_current)

    def iniciar_Time(self):
        self.time_inicio = Clock.get_time()
        logging.debug('iniciar_time: time iniciado ({})'.format(self.time_inicio))

    def tempo_decorrido_inicio(self):
        self.tempo_decorrido = Clock.get_time() - self.time_inicio
        self.tempo_decorrido_str = "Tempo decorrido do início: {0:.2f}".format(self.tempo_decorrido) + ' segundos'
        return self.tempo_decorrido

    def iniciar_treinos(self):
        self.iniciar_Time()
        self.gerar_resultlog_file()
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

    def generate_next_tela(self, proxima):
        logging.debug('generate_next_tela: next tela {}'.format(proxima))
        if 'Teste' in proxima:
            if 'AB' in proxima:
                tela = TelaTesteTTAB(name=proxima, combinacoes=self.all_combinacoes_XY[self.tela_AB_current],
                                     ordem=self.ordem)
                logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                return tela
            else:
                tela = TelaTesteTTDE(name=proxima, combinacoes=self.all_combinacoes_ZW[self.tela_DE_current],
                                     ordem=self.ordem)
                logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                return tela
        elif 'Treino' in proxima:
            if self.isMisto:
                if self.current_treino_misto is 'BC':
                    if 'AB' in proxima:
                        tela = TelaTreinoAB(name=proxima,
                                            combinacoes=self.all_combinacoes_XY_mistoBC[self.tela_misto_AB_current],
                                            ordem=self.ordem)
                        logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                        return tela
                    else:
                        tela = TelaTreinoDE(name=proxima,
                                            combinacoes=self.all_combinacoes_ZW_mistoEF[self.tela_misto_DE_current],
                                            ordem=self.ordem)
                        logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                        return tela
                else:
                    if 'AB' in proxima:
                        tela = TelaTreinoAB(name=proxima,
                                            combinacoes=self.all_combinacoes_XY_mistoAB[self.tela_misto_AB_current],
                                            ordem=self.ordem)
                        logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                        return tela
                    else:
                        tela = TelaTreinoDE(name=proxima,
                                            combinacoes=self.all_combinacoes_ZW_mistoDE[self.tela_misto_DE_current],
                                            ordem=self.ordem)
                        logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                        return tela
            else:
                if 'AB' in proxima:
                    tela = TelaTreinoAB(name=proxima, combinacoes=self.all_combinacoes_XY[self.tela_AB_current],
                                        ordem=self.ordem)
                    logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                    return tela
                else:
                    tela = TelaTreinoDE(name=proxima, combinacoes=self.all_combinacoes_ZW[self.tela_DE_current],
                                        ordem=self.ordem)
                    logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
                    return tela
        else:
            tela = TelaFinal(name='tela_final')
            logging.debug('generate_next_tela Gerada tela {} {}'.format(tela.name, tela))
            return tela

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
        if self.total_acertoserros_necessarios_saida == self.total_hits_necessarios_saida or tempo_decorrido >= self.tempo_maximo:
            tela_final = ''
            logging.debug('Main.troca_tela: total de acertos/erros {} letters {}.'.format(
                self.total_acertoserros_necessarios_saida, self.letters))
            logging.debug('Main.troca_tela: tela final sera chamada {}.'.format(tela_final))
            self.finalizar_result_file()
            self.acertos_total = 0
            self.acertos_total_str = str(self.acertos_total)
            self.erros_total = 0
            self.erros_total_str = str(self.erros_total)
            self.add_widget(TelaFinal(name=tela_final))
            self.current = tela_final
        else:
            if 'TT' in self.letters:
                logging.debug('Main.troca_tela: total de acertos/erros até o momento é {} letters {}.'.format(
                    self.total_acertoserros_necessarios_saida, self.letters))
            else:

                logging.debug('Main.troca_tela: total de acertos até o momento é {}.'.format(
                    self.total_acertoserros_necessarios_saida, self.letters))
            tela_atual = self.current
            self.ultima = self.current

            if self.tela_AB_finished:
                self.tela_AB_finished = False
                proxima = self.screen_name_DE + self.get_next_tela(self.screen_name_DE, self.isMisto)
                print(proxima)
                logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                self.adiciona_tela(self.generate_next_tela(proxima))
                self.proxima = proxima

                # add blanktela and add schedule
                self.show_blanktela(1.5)

            if self.tela_DE_finished:
                self.tela_DE_finished = False
                if self.tela_DE_respondidas == 3:
                    self.tela_DE_respondidas = 0
                    if self.isMisto:
                        if self.current_treino_misto is 'AB':
                            self.current_treino_misto = 'BC'
                        else:
                            self.current_treino_misto = 'AB'

                    proxima = self.screen_name_AB + self.get_next_tela(self.screen_name_AB, self.isMisto)
                    self.adiciona_tela(self.generate_next_tela(proxima))

                    logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                    self.proxima = proxima

                    # add blanktela and add schedule
                    self.show_blanktela(0.5)
                else:
                    proxima = self.screen_name_DE + self.get_next_tela(self.screen_name_DE, self.isMisto)
                    self.adiciona_tela(self.generate_next_tela(proxima))
                    logging.debug('Main.troca_tela: trocando da tela {} para {}'.format(tela_atual, proxima))
                    self.proxima = proxima

                    # add blanktela and add schedule
                    self.show_blanktela(0.5)

    def show_blanktela(self, timeout):
        self.add_widget(BlankTela(name='blanktela'))
        self.current = 'blanktela'
        Clock.schedule_once(self.apagar_blanktela, timeout)

    def apagar_blanktela(self, delta_time):
        logging.debug('remove_tela: tela {} apagada'.format("blanktela"))
        self.current = self.proxima
        self.remove_tela(self.ultima)
        self.remove_tela("blanktela")

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

    def build(self):
        self.title = 'TRTT'
        return GerenciadorDeTelas()


Main().run()
