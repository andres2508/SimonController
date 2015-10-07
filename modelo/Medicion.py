import json

__author__ = 'Andres'

import time


class Medicion:
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self, tipo_medicion, url_medicion, start_freq, final_freq, canalization, span_device):
        self.tipo_medicion = tipo_medicion
        self.url_medicion = url_medicion
        self.start_freq = start_freq
        self.final_freq = final_freq
        self.canalization = canalization
        self.span_device = span_device
        self.isRun = False
        self.service_id = "No se que es"
        self.timestamp = time.strftime("%H:%M:%S")
        self.result = ""
        self.id = ""
    ##---------------------------------------------------------------------------------
    ##  Metodos
    ##---------------------------------------------------------------------------------

    def correr_medicion(self):
        return False


    def terminar_medicion(self):
        self.isRun = True

    def generar_json(self):
        data = {'id_measure': self.id, 'start_freq': self.start_freq, 'stop_freq': self.final_freq,
                "result": self.result}
        json_data = json.dumps(data)

        return json_data

