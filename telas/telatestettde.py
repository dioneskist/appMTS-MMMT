import logging
import os
import random
from datetime import datetime
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Callback
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from elements.attempt import Attempt
from elements.elements import SourcePicture, TargetPicture, Imagem


class TelaTesteTTDE(Screen):
    targetPictures = ListProperty(None)
    sourcePictures = ListProperty(None)
    images = ListProperty(None)

    # variaveis utilizadas na inicializacao de uma nova tentativa
    ordem = StringProperty('teste')
    combinacoes = ListProperty()
    acertos = 0
    erros = 0
    telaatual = StringProperty()
    start_screen_time = None
    timeout_screen_blocker = 1.0
    timeout_troca_tela = 0.0
    timeout_troca_tela_last_element = 0.0

    should_show_smile = False
    isTT = True
    screen_blocked = False

    def __init__(self, **kw):
        super(TelaTesteTTDE, self).__init__(**kw)

        logging.debug('TelaTesteTTDE.__init__:')
        logging.debug('TelaTesteTTDE.__init__: combinacoes {}'.format(self.combinacoes))

    def on_enter(self, *args):
        # popula imagens inicias
        self.popula_imagens_target()
        self.popula_imagens_source()
        logging.debug('tela: {} com ids: {}'.format(self.name, self.ids))
        self.start_screen_time = datetime.now()
        self.telaatual = self.parent.current

    def on_leave(self, *args):
        logging.debug('on_leave: {} com ids: {}'.format(self.name, self.ids))

    # popular imagens para todos os sourcesPictures
    # a_1
    # b_2
    def popula_imagens_source(self):
        self.ids._si1._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(1) + '.jpg'
        self.ids._si2._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(2) + '.jpg'
        self.ids._si3._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(3) + '.jpg'

    # popular imagens para todos os targetPictures
    # a_1
    # b_2
    def popula_imagens_target(self):
        self.ids._ti1._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_target() + '.jpg'

    def get_figura_target(self):
        figura = self.combinacoes[0]
        logging.debug('get_figura_target: pegando figura target {} '.format(figura))
        return figura

    def get_figura_source(self, posicao):
        figura = self.combinacoes[posicao]
        logging.debug('get_figura_source: pegando figura source {}'.format(figura))
        return figura

    # return three values
    # collision status (true, false)
    # id widget drag source
    # id widget drag source
    def check_for_collisions(self, moving_widget):
        for otherWidget in self.targetPictures:
            if moving_widget.collide_widget(otherWidget):
                logging.debug('Collision detected between [' + moving_widget.wid + '][' + otherWidget.wid + ']')
                # print(otherWidget.wid)
                # otherWidget.wid
                return True, moving_widget.wid, otherWidget.wid
        return False, 0, 0

    def acertou(self, collision, id_widget_source, id_widget_target):
        logging.debug('acertou: iniciando com {} {} {}'.format(collision, id_widget_source, id_widget_target))
        if collision:
            # extrai numero do wid para validar se figura é mesma.
            # basta somente ser o mesmo numero que está correto
            # ex: a figura do wid wid-si1 tem o mesmo numero da figura do wid-ti1 esta ok
            # ex: a figura do wid wid-si2 tem o mesmo numero da figura do wid-ti2 esta ok
            # ex: a figura do wid wid-si3 NAO tem o mesmo numero da figura do wid-ti32 NAO ok
            ln_figura_s = self.get_imagens_source('wid-si' + str(id_widget_source[len(id_widget_source) - 1]))
            ln_figura_t = self.get_imagens_target('wid-ti' + str(id_widget_target[len(id_widget_target) - 1]))
            numero_figura_s = ln_figura_s[1]
            numero_figura_t = ln_figura_t[1]

            logging.debug('acertou: serao validadas os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))
            if numero_figura_s == numero_figura_t:
                logging.debug(
                    'acertou: IGUAIS -- os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))
                return True
            else:
                logging.debug(
                    'acertou: ERROU -- os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))
        else:
            print('nao bateu em nada. Printar ND no relatorio ({} ND)'.format(id_widget_source))

    def get_imagens_source(self, wid):
        logging.debug('get_imagens_source: iniciando {}'.format(wid))
        # carrega filhos do world (target, source, smile)
        for child in self.children:
            # print(id(c))
            # print(c.wid)
            if type(child) == SourcePicture:
                # carrega filhos do source (imagem)
                for image in child.children:
                    if (image.__self__.wid == wid):
                        logging.debug('get_imagens_source: validando wid=[{}] e imagem {}'.format(image.__self__.wid,
                                                                                                  image.__self__.source))
                        return self.get_letter_and_number_from_source(image.__self__.source)

    def get_letter_and_number_from_source(self, source):
        # figuras/teste/b_3.jpg
        s = source.split('/')[2]
        ln = s[0]
        nn = s[2]
        logging.debug(
            'get_number_from_source: extraido letter {} and number {} da imagem com nome: {}'.format(ln, nn, source))
        return ln + nn

    def get_imagens_target(self, wid):
        logging.debug('get_imagens_target: iniciando {}'.format(wid))
        # carrega filhos do world (target, source, smile)
        for child in self.children:
            # print(id(c))
            # print(c.wid)
            if type(child) == TargetPicture:
                # carrega filhos do source (imagem)
                for image in child.children:
                    # print(image.__self__.wid)
                    if (image.__self__.wid == wid):
                        logging.debug('get_imagens_source: validando wid=[{}] e imagem {}'.format(image.__self__.wid,
                                                                                                  image.__self__.source))
                        # print(image.__self__.source)
                        return self.get_letter_and_number_from_source(image.__self__.source)

    def colocar_source_na_origem(self, id_widget_source):
        logging.debug('colocar_source_na_origem: app size: {}wX{}h'.format(self.width, self.height))
        logging.debug('colocar_source_na_origem: Reorganizando sourcePicture wid=[{}]'.format(id_widget_source))
        if id_widget_source == 'wid-s1':
            self.ids._s1.pos = 80, 200
            logging.debug('colocar_source_na_origem: colocado wid [{}] na posicao x={}, y={}'.format(self.ids._s1.wid,
                                                                                                     self.ids._s1.pos[
                                                                                                         0],
                                                                                                     self.ids._s1.pos[
                                                                                                         1]))
        if id_widget_source == 'wid-s2':
            self.ids._s2.pos = 80, 840
            logging.debug('colocar_source_na_origem: colocado wid [{}] na posicao x={}, y={}'.format(self.ids._s2.wid,
                                                                                                     self.ids._s2.pos[
                                                                                                         0],
                                                                                                     self.ids._s2.pos[
                                                                                                         1]))
        if id_widget_source == 'wid-s3':
            self.ids._s3.pos = 80, 1480
            logging.debug('colocar_source_na_origem: colocado wid [{}] na posicao x={}, y={}'.format(self.ids._s3.wid,
                                                                                                     self.ids._s3.pos[
                                                                                                         0],
                                                                                                     self.ids._s3.pos[
                                                                                                         1]))

    def show_smile(self, number):
        if self.should_show_smile:
            logging.debug('show_smile: colocando smile {}'.format(number))
            if int(number) == 1:
                self.ids._smile1.source = 'figuras/smile.png'
                apagar_widget_id = self.ids._smile1
                self.desaparecer_smile(apagar_widget_id)
        else:
            logging.debug('show_smile: smile doesn\'t show for Test TT, but the block time is the same'.format())
            Clock.schedule_once(self.schedule_time, self.timeout_screen_block)
            self.incrementa_acerto()
            self.screen_blocked = True

    def schedule_time(self, delta):
        pass

    def desaparecer_smile(self, apagar_widget_id):
        logging.debug('desaparecer_smile: smile a ser retirado wis={}'.format(apagar_widget_id))
        callback = self.apagar_smiles
        logging.debug(
            'desaparecer_smile: scheduled {} with {} timeout for smile wid={}'.format(callback.__name__, self.timeout_screen_blocker,
                                                                                      apagar_widget_id))
        Clock.schedule_once(partial(callback, apagar_widget_id, apagar_widget_id), self.timeout_screen_blocker)

    def apagar_smiles(self, apagar_widget_id, *args, **keywords):
        logging.debug('apagar_smiles: removido smiles wid={}'.format(apagar_widget_id))
        self.remove_widget(apagar_widget_id)
        self.incrementa_acerto()

    def incrementa_erro(self):
        logging.debug(
            'TelaTesteTTDE.incrementa_erro: incrementando erros de {} para {}'.format(self.erros, self.erros + 1))
        self.erros += 1
        self.manager.acertos_total = 0
        self.manager.total_acertoserros_necessarios_saida += 1
        self.manager.erros_total += 1
        self.manager.erros_consecutivos()
        self.validate_troca_tela()

    def write_attempt(self, hit_error, id_widget_source, id_widget_target):
        logging.debug(
            'TelaTesteTTDE.write_attempt: writing attempt Hit?{}:{} {}-{}'.format(hit_error, hit_error.value,
                                                                                  id_widget_source, id_widget_target))

        letter_number_figura_s = self.get_imagens_source('wid-si' + str(id_widget_source[len(id_widget_source) - 1]))
        letter_number_figura_t = self.get_imagens_target('wid-ti' + str(id_widget_target[len(id_widget_target) - 1]))

        # key_comparation is the position on the screen in inverter order
        # position 1 return 3; 2 return 2 and 3 return 1
        attempt = Attempt(comparation=str(letter_number_figura_s).upper(),
                          key_comparation=get_position(id_widget_source[len(id_widget_source) - 1]),
                          model=str(letter_number_figura_t).upper(),
                          key_model=get_position(id_widget_target[len(id_widget_target) - 1]),
                          hit_or_error=hit_error.value,
                          latency_from_screen=datetime.now() - self.start_screen_time,
                          consecutive_hits=self.manager.consecutive_hists)

        print(attempt)
        self.manager.write_attempt(attempt, self.name)

    def incrementa_acerto(self):
        logging.debug(
            'TelaTesteTTDE.incrementa_acerto: incrementando acertos de {} para {}'.format(self.acertos,
                                                                                          self.acertos + 1))
        self.acertos += 1
        self.manager.acertos_total += 1
        self.manager.total_acertoserros_necessarios_saida += 1
        self.manager.acertos_consecutivos()
        self.validate_troca_tela()

    def validate_troca_tela(self):
        if not self.isTT:
            if self.acertos == 1:
                self.screen_blocked = True
                logging.info('TelaTesteTTDE.incrementa_acerto: ACERTOU TUDO ({} acertos) !!!'.format(self.acertos))
                # if self.manager.tela_DE_respondidas == 2:
                #     Clock.schedule_once(self.troca_tela, self.timeout_troca_tela_last_element)
                # else:
                Clock.schedule_once(self.troca_tela, self.timeout_troca_tela)
        else:
            if self.acertos == 1 or self.erros == 1:
                self.screen_blocked = True
                logging.info('TelaTesteTTAB.incrementa_acerto+erro: isTT ({}+{} acertos + erros = {}) !!!'.format(
                    self.acertos, self.erros, self.acertos + self.erros))
                # if self.manager.tela_DE_respondidas == 2:
                #     Clock.schedule_once(self.troca_tela, self.timeout_troca_tela_last_element)
                # else:
                Clock.schedule_once(self.troca_tela, self.timeout_troca_tela)

    def troca_tela(self, delta):
        self.screen_blocked = False
        self.manager.tela_DE_finished = True
        self.manager.tela_DE_respondidas += 1
        self.manager.troca_tela()


def get_position(wid):
    return '2'
