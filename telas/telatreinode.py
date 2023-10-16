import logging
import os
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Callback
from kivy.properties import ListProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from elements.elements import SourcePicture, TargetPicture, Imagem


class TelaTreinoDE(Screen):
    targetPictures = ListProperty(None)
    sourcePictures = ListProperty(None)
    images = ListProperty(None)

    # variaveis utilizadas na inicializacao de uma nova tentativa
    ordem = StringProperty('teste')
    combinacoes = ListProperty()
    acertos = 0
    erros = 0

    def __init__(self, **kw):
        super(TelaTreinoDE, self).__init__(**kw)

        logging.debug('TelaTreinoDE.__init__:')
        logging.debug('TelaTreinoDE.__init__: combinacoes {}'.format(self.combinacoes))

    def on_enter(self, *args):
        # popula imagens inicias
        self.popula_imagens_target()
        self.popula_imagens_source()
        logging.debug('tela: {} com ids: {}'.format(self.name, self.ids))
        self.manager.latencia = Clock.get_time()

    def on_leave(self, *args):
        logging.debug('on_leave: {} com ids: {}'.format(self.name, self.ids))

    # popular imagens para todos os sourcesPictures
    # a_1
    # b_2
    def popula_imagens_source(self):
        self.ids._si1._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(1) + '.jpg'
        print(self.ids._si1._imagem)
        print(self.get_figura_source(1))
        self.ids._si2._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(2) + '.jpg'
        print(self.ids._si2._imagem)
        print(self.get_figura_source(2))
        self.ids._si3._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_source(3) + '.jpg'
        print(self.ids._si3._imagem)
        print(self.get_figura_source(3))
        # logging.debug('popula_imagens_source: Iniciando carregamento da imagens para sourcePictures')
        # logging.debug('popula_imagens_source: Existem {} combinacoes'.format(self.combinacoes))
        # # carrega filhos do world (target, source, smile)
        # contador_figura = 0
        # for child in self.children:
        #     if type(child) == SourcePicture:
        #         # carrega filhos do source (imagem)
        #         for image in child.children:
        #             figura = self.get_figura_source(contador_figura)
        #             logging.debug('popula_imagens_source: Associada figura {} com wid=[{}]'.format(figura, image.wid))
        #             imagem_name = 'figuras/' + self.ordem + '/' + figura + '.jpg'
        #             image.__self__._imagem = imagem_name
        #             contador_figura += 1

    # popular imagens para todos os targetPictures
    # a_1
    # b_2
    def popula_imagens_target(self):
        self.ids._ti1._imagem = 'figuras/' + self.ordem + '/' + self.get_figura_target() + '.jpg'
        print(self.ids._ti1._imagem)
        print(self.get_figura_target())
        # logging.debug('popula_imagens_target: Iniciando carregamento da imagens para targetPictures')
        # logging.debug('popula_imagens_target: Existem {} combinacoes'.format(self.combinacoes))
        # # carrega filhos do world (target, source, smile)
        # for child in self.children:
        #     # print(id(child))
        #     # print(type(child))
        #     if type(child) == TargetPicture:
        #         # carrega filhos do target (imagem)
        #         for image in child.children:
        #             figura = self.get_figura_target()
        #             logging.debug('popula_imagens_target: Associada figura {} com wid=[{}]'.format(figura, image.wid))
        #             imagem_name = 'figuras/' + self.ordem + '/' + figura + '.jpg'
        #             image.__self__._imagem = imagem_name

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
            numero_figura_s = self.get_imagens_source('wid-si' + str(id_widget_source[len(id_widget_source) - 1]))
            numero_figura_t = self.get_imagens_target('wid-ti' + str(id_widget_target[len(id_widget_target) - 1]))
            logging.debug('acertou: serao validadas os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))
            if numero_figura_s == numero_figura_t:
                logging.debug(
                    'acertou: IGUAIS -- os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))
                return True
            else:
                logging.debug(
                    'acertou: ERROU -- os numeros [{}] e [{}]'.format(numero_figura_s, numero_figura_t))

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
                        return self.get_number_from_source(image.__self__.source)

    def get_number_from_source(self, source):
        # figuras/teste/b_3.jpg
        s = source.split('_')
        n = s[1].split('.')
        logging.debug('get_number_from_source: extraido numero {} da imagem com nome: {}'.format(n[0], source))
        return n[0]

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
                        return self.get_number_from_source(image.__self__.source)

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
        logging.debug('show_smile: colocando smile {}'.format(number))
        if int(number) == 1:
            self.ids._smile1.source = 'figuras/smile.png'
            self.apagar_widget_id = self.ids._smile1
            self.desaparecer_smile()

    def desaparecer_smile(self):
        logging.debug('desaparecer_smile: smile a ser retirado')
        Clock.schedule_interval(self.apagar_smiles, 2.0)

    def apagar_smiles(self, delta_time):
        if self.apagar_widget_id is not None:
            logging.debug('apagar_smiles: removendo {}'.format(self.apagar_widget_id))
            self.remove_widget(self.apagar_widget_id)
            self.apagar_widget_id = None
            Clock.unschedule(self.apagar_smiles)

    def incrementa_erro(self):
        logging.debug('Telateste.incrementa_erro: incrementando erros de {} para {}'.format(self.erros, self.erros + 1))
        self.erros += 1
        self.manager.acertos_total = 0
        self.manager.acertos_total_str = 'Acertos:  ' + str(self.manager.acertos_total)
        self.manager.erros_total += 1
        self.manager.erros_total_str = 'Erros:  ' + str(self.manager.erros_total)
        self.manager.latencia_erro_str = "Latencia erro: {0:.2f}".format(
            Clock.get_time() - self.manager.latencia) + ' segundos'

    def incrementa_acerto(self):
        logging.debug(
            'Telateste.incrementa_acerto: incrementando acertos de {} para {}'.format(self.acertos, self.acertos + 1))
        self.acertos += 1
        self.manager.acertos_total += 1
        self.manager.acertos_total_str = 'Acertos:  ' + str(self.manager.acertos_total)
        self.manager.latencia_acerto_str = "Latência: {0:.2f}".format(
            Clock.get_time() - self.manager.latencia) + ' segundos'
        if self.acertos == 1:
            logging.info('Telateste.incrementa_acerto: ACERTOU TUDO ({} acertos) !!!'.format(self.acertos))
            Clock.schedule_interval(self.troca_tela, 1.0)

    def troca_tela(self, delta):
        Clock.unschedule(self.troca_tela)
        self.manager.tela_treinoDE_finished = True
        self.manager.tela_treinoDE_respondidas += 1
        self.manager.troca_tela()
