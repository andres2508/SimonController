__author__ = 'Andres'

import SocketServer
import socket
# from modelo import Medicion
import Medicion
import threading
import json
import os
import urllib2


class Tarjeta:
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self, sc, tipo_tarjeta, direccion_ip, minimum_frequency, maximum_frequency, instant_bandwith):
        self.tipo_tarjeta = tipo_tarjeta
        self.id_tarjeta = 0
        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency
        self.instant_bandwith = instant_bandwith
        self.isDisponible = True
        self.direccion_ip = direccion_ip
        self.mediciones = []
        ###
        # Variables Servidor TCP
        ###

        self.socket = sc
        self.isConnected = True

    ##---------------------------------------------------------------------------------
    ## Funcionalidades
    ##---------------------------------------------------------------------------------

    def correr_funcion(self, funcion, measurement_id, start_frec, final_frec, canalization, span_device, time, samples):
        resultado = "Sin resultado"
        for i in range(0, samples):
            if funcion == "occ":
                nueva_medicion = Medicion.Medicion(funcion,
                                                   "funciones/" + self.tipo_tarjeta + "/Ocupacion/SIMONES_Ocupacion.py",
                                                   start_frec, final_frec, canalization,
                                                   span_device, measurement_id, time)
                resultado = nueva_medicion.correr_medicion(self.socket)
                self.grabar_samples_measurement(resultado, measurement_id, i)

                #         t = threading.Thread(target=nueva_medicion.correr_medicion, args=(self.socket,))
                #        t.start()
                #        self.mediciones.append(nueva_medicion)
        self.send_post_result(measurement_id, samples)


    def send_post_result(self,measurement_id,samples):
        data_json = None
        url = 'http://192.168.160.96:9999/post'
        for i in range(0, samples):
            file_name = str(measurement_id)+ "-" + str(i)
            with open("/home/andres/Escritorio/SimonController/modelo/results/"+file_name) as data_file:
                data_json = json.load(data_file)
		print "ESTE ES EL JSON"
		print data_json
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, data_json)



    def grabar_samples_measurement(self, resultado, measurement_id, counter):
        file_name = str(measurement_id) + "-" + str(counter)
        with open("/home/andres/Escritorio/SimonController/modelo/results/" + file_name, "w") as outfile:
            json.dump(resultado, outfile)

    def buscar_medicion(self, measurement_id):
        return "hola"

    ##---------------------------------------------------------------------------------
    ## Gets and Sets
    ##---------------------------------------------------------------------------------

    def getMinimum_Frecuency(self):
        return self.minimum_frecuency

    def getMaximum_Frecuency(self):
        return self.maximum_frecuency

    def getInstant_Bandwith(self):
        return self.instant_bandwith

    def isDisponible(self):
        return self.isDisponible

    def setMinimum_Frecuency(self, minimum_frecuency):
        self.minimum_frecuency = minimum_frecuency

    def setMaximum_Frecuency(self, maximum_frecuency):
        self.maximum_frecuency = maximum_frecuency

    def getTipo_tarjeta(self):
        return self.tipo_tarjeta

    def getId_tarjeta(self):
        return self.id_tarjeta
