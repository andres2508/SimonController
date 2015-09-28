import socket

__author__ = 'Andres'

class Tarjeta_Cliente():

    def __init__(self):

        self.tipoTarjeta = 'bladeRF'

        ## Variables Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_server = 'localhost'
        self.host = socket.gethostbyname(self.ip_server)
        self.port = 1234
        self.tamano_paquetes = 1024

        self.inicializar_server()

    def inicializar_server(self):
        self.sock.connect((self.host, self.port))

    def protocolo(self):

        self.sock.send(self.tipoTarjeta)
        mensaje = str(self.sock.recv(self.tamano_paquetes))
        print ("Estado de la conexion: "+ mensaje)


    ##---------------------------------------------------------------------------------
    ##  Main
    ##---------------------------------------------------------------------------------

if __name__ == '__main__':
    mundo = Tarjeta_Cliente()
    mundo.protocolo()