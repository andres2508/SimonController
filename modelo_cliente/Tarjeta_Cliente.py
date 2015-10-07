import socket
import subprocess

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

        subproceso2.stdin.write(str(inicial_freq) + "\n")
        subproceso2.stdin.write(str(final_freq) + "\n")
        subproceso2.stdin.write(str(canalization) + "\n")
        subproceso2.stdin.write(str(span_device) + "\n")



    def protocolo(self):

        self.sock.send(self.tipoTarjeta)
        mensaje = str(self.sock.recv(self.tamano_paquetes))
        print ("Estado de la conexion: "+ mensaje)

        mensaje = str(self.sock.recv(self.tamano_paquetes))

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
    mundo.protocolo()