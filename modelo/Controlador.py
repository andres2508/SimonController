import os

__author__ = 'Andres'

import subprocess
import threading
import time
import socket
from modelo import Tarjeta


class Controlador(object):
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self):
        self.t = None
        self.terminar = None
        self.blade = None

        ###
        # Variables Server
        ##
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_server = ''
        self.host = socket.gethostbyname(self.ip_server)
        self.port = 1234
        self.cant_embebidos = 5
        self.tamano_paquetes = 1024

        self.inicializar_server()
        self.tarjetas = []


    ##---------------------------------------------------------------------------------
    ##  Metodo Server Socket
    ##---------------------------------------------------------------------------------

    def inicializar_server(self):
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(self.cant_embebidos)

    def protocolo_inicial(self):

        for i in range(0, self.cant_embebidos):

            sc, addr = self.serverSocket.accept()
            print('Recibi una conexion de ', addr)
            tipoTarjeta = str(sc.recv(self.tamano_paquetes))

            self.inicializar_tarjeta(tipoTarjeta, addr, sc)
            sc.send("OK")

    def inicializar_tarjeta(self, tipoTarjeta, direccion_ip, sc):

        ##print('./config'+str(tipoTarjeta))
        archive = open('config/'+tipoTarjeta, 'r')

        linea = archive.readline().split("=")
        minimum_frequency = linea[1]

        linea = archive.readline().split("=")
        maximum_frequency = linea[1]

        linea = archive.readline().split("=")
        instant_bandwith = linea[1]

        nuevaTarjeta = Tarjeta.Tarjeta(sc, tipoTarjeta, direccion_ip, minimum_frequency, maximum_frequency, instant_bandwith)
        self.tarjetas.append(nuevaTarjeta)

    ##---------------------------------------------------------------------------------
    ##  Metodos
    ##---------------------------------------------------------------------------------

    def subproceso(self, proceso, tiempo):
        # self.p = subprocess.Popen(proceso,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.t = threading.Thread(target=self.correr_blade, args=(tiempo, proceso,))
        self.t.start()
        print "termino start"
        # Es necesario este tiempo porque el subproceso se demora 20 segundos en iniciar la blade
        return self.t

    def correr_blade(self, tiempo, proceso):
        # blade = i2t_udp_synchronization_power_bladeRF()
        self.blade = subprocess.Popen(proceso, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(20)
        ## .............................................
        ## Siempre que mandes algo dale un salto de linea
        ## ..............................................
        self.blade.stdin.write(str(tiempo) + "\n")
        self.blade.stdin.flush()
        cadena = "Ok"
        self.terminar = False
        while cadena != "Finish\n" and self.terminar != True:
            self.blade.stdin.write("Ok\n")
            self.blade.stdin.flush()
            cadena = self.blade.stdout.readline()
            print "Estado terminar: " + str(self.terminar)

        if self.terminar:
            self.blade.stdin.write("Stop\n")
            print "Escribio Stop"

    def terminar_proceso(self):
        self.terminar = True
        return "Termino proceso"

    ##---------------------------------------------------------------------------------
    ##  Main
    ##---------------------------------------------------------------------------------

if __name__ == '__main__':

    variable = os.getcwd()
    os.chdir('C:/Users/Andres/Dropbox/TRABAJO/i2t/Simon Controler/')
    mundo = Controlador()
    ##mundo.inicializar_tarjeta('bladeRF', '192.168.1.1')

    mundo.protocolo_inicial()