import socket
import subprocess
import os


__author__ = 'Andres'

class Tarjeta_Cliente():

    def __init__(self):

        self.tipoTarjeta = 'bladeRF'
        self.tipoControlador = 'CubieBoard'

        ## Variables Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_server = 'localhost'
        self.host = socket.gethostbyname(self.ip_server)
        self.port = 1234
        self.tamano_paquetes = 1024

        self.inicializar_server()

    def inicializar_server(self):
        self.sock.connect((self.host, self.port))

    def correr_occupation(self, inicial_freq, final_freq, canalization, span_device):

        subproceso1 = subprocess.Popen("python /funciones/"+self.tipoControlador+"/"+self.tipoTarjeta
                                      +"/Ocupacion/SIMONES_Occupation.py",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

        subproceso2 = subprocess.Popen("python /funciones/"+self.tipoControlador+"/"+self.tipoTarjeta
                                      +"/Ocupacion/Fusion_Center_Occupation.py",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

        print(str(inicial_freq) + str('\n'))
        subproceso2.stdin.write(inicial_freq + '\n')
        subproceso2.stdin.write(str(final_freq) + str("\n"))
        subproceso2.stdin.write(str(canalization) + str("\n"))
        subproceso2.stdin.write(str(span_device) + str("\n"))



    def protocolo(self):

        self.sock.send(self.tipoTarjeta)
        mensaje = str(self.sock.recv(self.tamano_paquetes))
        print ("Estado de la conexion: "+ mensaje)
        self.sock.send("Escucho peticion")
        mensaje = str(self.sock.recv(self.tamano_paquetes))
        print("llego la siguiente medicion: "+ mensaje)
        self.sock.send("OK")
        if mensaje == "Ejecutar Medicion":
            mensaje = str(self.sock.recv(self.tamano_paquetes))
            arreglo = mensaje.split(";")

            if arreglo[0] == "occ":
                self.correr_occupation(arreglo[1],arreglo[2],arreglo[3],arreglo[4])
                print("Corriendo occ")


    ##---------------------------------------------------------------------------------
    ##  Main
    ##---------------------------------------------------------------------------------

if __name__ == '__main__':
    mundo = Tarjeta_Cliente()
    os.chdir('C:/Users/Andres/Dropbox/TRABAJO/i2t/Simon Controler/')
    mundo.protocolo()