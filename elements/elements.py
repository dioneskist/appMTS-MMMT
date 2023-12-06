import logging
from kivy.properties import StringProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.label import Label

from elements.enum.hiterror import HitError

red = [1, 0, 0, 1]
light_blue = [0, 0.5, 1, 1]
yellow = [1, 1, 0, 1]
white = [1, 1, 1, 1]


class TargetPicture(Label):
    rbgcolor = ListProperty(white)


class Imagem(Image):
    _imagem = StringProperty()


class SourcePicture(Label):
    rbgcolor = ListProperty(white)

    #
    # #imagens
    # _imagems1 = StringProperty('figuras/teste/b_1.jpg')
    # _imagems2 = StringProperty('figuras/teste/b_2.jpg')
    # _imagems3 = StringProperty('figuras/teste/b_3.jpg')

    # imagens = carregar_figuras('ordem1', "a", "b")

    def __init__(self, **kwargs):
        super(SourcePicture, self).__init__(**kwargs)
        self.clicked_wid = None
        self.touchedMe = False

    def on_touch_down(self, touch):
        if not self.parent.screen_blocked:
            self.touchedMe = self.collide_point(touch.x, touch.y)
            if self.touchedMe:
                logging.debug('on_touch_down: Clicked in wid=[{}]'.format(self.wid))
                self.clicked_wid = self.wid
            else:
                logging.debug('on_touch_down: Clicked in nothing')
        else:
            logging.debug('on_touch_down: screen Blocked')

    def on_touch_up(self, touch):

        if self.touchedMe:
            # confere se colidiu
            collision, id_widget_source, id_widget_target = self.parent.check_for_collisions(self)
            logging.debug('on_touch_up: collision={}, id_widget_source=[{}], id_widget_target=[{}]'.format(collision,
                                                                                                           id_widget_source,
                                                                                                           id_widget_target))
            if self.parent.acertou(collision, id_widget_source, id_widget_target):
                logging.debug('on_touch_up: acertou')
                self.reset_colors()
                # coloca source na origem
                # self.parent.colocar_source_na_origem(self.clicked_wid)
                self.parent.manager.acertos_consecutivos()
                self.parent.show_smile(id_widget_target[len(id_widget_target) - 1])
                self.parent.write_attempt(HitError.HIT, id_widget_source, id_widget_target)
                self.parent.remove_widget(self)
                self.touchedMe = False

            else:
                self.reset_colors()
                self.parent.colocar_source_na_origem(self.clicked_wid)
                if collision:
                    self.parent.incrementa_erro()
                    self.parent.write_attempt(HitError.ERROR, id_widget_source, id_widget_target)
                    if self.parent.isTT:
                        self.parent.remove_widget(self)
                self.touchedMe = False

        else:
            self.touchedMe = False


    def on_touch_move(self, touch):
        if self.touchedMe:
            # print(self.width, self.height)
            # print(touch)
            self.pos[0] = touch.pos[0] - self.width / 2
            self.pos[1] = touch.pos[1] - self.height / 2
            collision, id_widget_source, id_widget_target = self.parent.check_for_collisions(self)
            if collision:
                if id_widget_target == 'wid-t3':
                    logging.debug('on_touch_move: comparing [' + id_widget_source + '] with [' + id_widget_target + ']')
                    self.parent.ids._t3.rbgcolor = yellow
                if id_widget_target == 'wid-t2':
                    logging.debug('on_touch_move: comparing [' + id_widget_source + '] with [' + id_widget_target + ']')
                    self.parent.ids._t2.rbgcolor = yellow
                if id_widget_target == 'wid-t1':
                    logging.debug('on_touch_move: comparing [' + id_widget_source + '] with [' + id_widget_target + ']')
                    self.parent.ids._t1.rbgcolor = yellow
            else:
                self.reset_colors()

    def reset_colors(self):
        self.reset_color_for_target('_t1')
        self.reset_color_for_target('_t2')
        self.reset_color_for_target('_t3')

    def reset_color_for_target(self, target_wid):
        try:
            self.parent.ids[target_wid].rbgcolor = white
        except:
            logging.debug('reset_color_for_target: {} nao existe'.format(target_wid))

    def on__imagem(self, instance, new_texture):
        self.rect.texture = new_texture
