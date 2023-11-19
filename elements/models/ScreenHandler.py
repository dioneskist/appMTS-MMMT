from abc import abstractmethod
from datetime import datetime, timedelta

from kivy.uix.screenmanager import ScreenManager

from telas.telatestettab import TelaTesteTTAB
from utils.screen_combinations import preparar_combinacoes


class ScreenHandler(ScreenManager):
    test_name: str # 'TT AB/DE'
    ordem: str
    number_hits_to_end: int
    timeout: float

    start_test_time: datetime
    end_test_time: datetime
    latency_test: timedelta

    @abstractmethod
    def run(self):
        super(ScreenManager, self).run()

    @abstractmethod
    def finish(self):
        pass

    @abstractmethod
    def generate_latency_from_screen(self):
        pass
    @abstractmethod
    def set_latency_end_time(self):
        pass