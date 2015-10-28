
__author__ = 'Andres'

import time
import socket
import json

class Medicion:
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self, tipo_medicion, url_medicion, start_freq, final_freq, canalization, span_device, id, time_measurement):
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
        self.id = id
	self.time = time_measurement
        self.packet_size = 536870912
    ##---------------------------------------------------------------------------------
    ##  Metodos
    ##---------------------------------------------------------------------------------

    def correr_medicion(self, socketCliente):
        self.isRun = True
        socketCliente.send("Ejecutar Medicion")
        mensaje = str(socketCliente.recv(self.packet_size))
        #print("Estado de ejecucion: "+)
        socketCliente.send(str(self.tipo_medicion)+';' + str(self.start_freq)+';'+str(self.final_freq)+';'+str(self.canalization)+';'+str(self.span_device)+';'+str(self.time))
        mensaje = str(socketCliente.recv(self.packet_size))
        #print("Estado de ejecucion: "+str(self.socketCliente.recv(self.packet_size)))
        #line = socketCliente.recv(self.packet_size)
        self.result = mensaje
#	print(self.result)
        self.isRun = False
	return self.result

    def terminar_medicion(self):
        self.isRun = True

    def generar_json(self):
        data = {'id_measure': self.id, 'start_freq': self.start_freq, 'stop_freq': self.final_freq,
                "result": self.result}
        json_data = json.dumps(data)

        return json_data

