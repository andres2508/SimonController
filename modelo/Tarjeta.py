__author__ = 'Andres'

import SocketServer
import socket
from modelo import Medicion

class Tarjeta:

    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self, sc, tipo_tarjeta, direccion_ip, minimum_frequency, maximum_frequency, instant_bandwith):

        self.tipo_tarjeta = tipo_tarjeta
        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency
        self.instant_bandwith = instant_bandwith
        self.isDisponible = True
        self.direccion_ip = direccion_ip
        self.mediciones = []
        ###
        # Variables Servidor TCP
        ###

        self.socket = socket
        self.isConnected = True

    ##---------------------------------------------------------------------------------
    ## Funcionalidades
    ##---------------------------------------------------------------------------------

    def correr_funcion(self, funcion, start_frec, final_frec, canalization, span_device):

        if funcion == "occ":
            nueva_medicion = Medicion.Medicion(funcion,"funciones/"+self.tipo_tarjeta+"/Ocupacion/SIMONES_Ocupacion.py",start_frec,final_frec,canalization,
                                               span_device)

            nueva_medicion.correr_medicion()
            self.mediciones.append(nueva_medicion)



    ##---------------------------------------------------------------------------------
    ## Gets and Sets
    ##---------------------------------------------------------------------------------

    def getMinimum_Frecuency(self):
        return self.maximum_frecuency

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

