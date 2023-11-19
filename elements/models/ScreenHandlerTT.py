from abc import abstractmethod
from datetime import datetime, timedelta

from kivy.uix.screenmanager import ScreenManager

from elements.models.ScreenHandler import ScreenHandler
from telas.telatestettab import TelaTesteTTAB
from utils.screen_combinations import preparar_combinacoes


class ScreenHandlerTT(ScreenHandler):

    def __init__(self, ordem, test_name, number_hits_to_end, timeout):
        self.ordem = ordem
        self.test_name = test_name
        self.number_hits_to_end = number_hits_to_end
        self.timeout = timeout
        self.all_combinacoes_XY, self.all_combinacoes_ZW = preparar_combinacoes(self.test_name)

        self.start_test_time = datetime.now()
        super(ScreenHandler, self).__init__()
        self.run()

    def run(self):
        super(ScreenHandler, self).run()
        hits = 0
        while hits < self.number_hits_to_end:

            s = TelaTesteTTAB(name=self.test_name + '_' + str(hits),
                              combinacoes=self.all_combinacoes_XY[hits],
                              ordem=self.ordem)
            self.add_widget(s)
            self.change_screen(s.name)

            if hits == self.number_hits_to_end - 1:
                self.finish()
            hits += 1

    def change_screen(self, tela):
        old = self.current
        if tela in self.screen_names:
            self.current = tela
            self.remove_widget(self.get_screen(old))
        else:
            raise Exception('Tela {} does not exist!'.format(tela))

    

    def finish(self):
        self.end_test_time = datetime.now()
        self.generate_latency_from_screen()

    def generate_latency_from_screen(self):
        self.latency_test = self.end_test_time - self.start_test_time
        return self.latency_test

    def export_result(self, report_format):
        pass
