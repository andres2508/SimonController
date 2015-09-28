__author__ = 'Andres'

import SocketServer
import socket

class Tarjeta:

    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self, tipo_tarjeta, direccion_ip, minimum_frequency, maximum_frequency, instant_bandwith):

        self.tipo_tarjeta = tipo_tarjeta
        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency
        self.instant_bandwith = instant_bandwith
        self.isDisponible = True
        self.isConnected = False
        self.direccion_ip = direccion_ip
        ###
        # Variables Servidor TCP
        ###

        self.socket = None

    ##---------------------------------------------------------------------------------
    ## Metodos Comunicacion Embebidos
    ##---------------------------------------------------------------------------------

    def inicializar_socket(self,socket):

        self.socket = socket
        self.isConnected = True

    ##---------------------------------------------------------------------------------
    ## Funcionalidades
    ##---------------------------------------------------------------------------------



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


