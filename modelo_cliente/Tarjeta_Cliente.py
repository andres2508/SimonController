import json
import socket
import subprocess
import os
import time

__author__ = 'Andres'


class Tarjeta_Cliente():
    def __init__(self):

        self.tipoTarjeta = 'bladeRF'
        self.tipoControlador = 'CubieBoard'

        ## Variables Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_server = '127.0.0.1'
        self.host = socket.gethostbyname(self.ip_server)
        self.port = 1234
        self.tamano_paquetes = 536870912

        self.inicializar_server()

    def inicializar_server(self):
        self.sock.connect((self.host, self.port))

    def correr_occupation(self, inicial_freq, final_freq, canalization, span_device, time_local):

        subproceso1 = subprocess.Popen(
            "python /home/andres/Escritorio/SimonController/funciones/" + self.tipoControlador + "/" + self.tipoTarjeta
            + "/Ocupacion/SIMONES_Occupation.py", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        time.sleep(12)

        subproceso2 = subprocess.Popen(
            "python /home/andres/Escritorio/SimonController/funciones/" + self.tipoControlador + "/" + self.tipoTarjeta
            + "/Ocupacion/Fusion_Center_Occupation.py", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(1)

        print("esta es la frecuencua inicial " + str(inicial_freq))
        print("esta es la frecuencua final " + str(final_freq))
        print("esta es la canalization " + str(canalization))
        print("esta es la span " + str(span_device))
        print("esta es el tiempo " + str(time_local))

        subproceso2.stdin.write(str(inicial_freq) + '\n')
        subproceso2.stdin.flush()

        subproceso2.stdin.write(str(final_freq) + str("\n"))
        subproceso2.stdin.flush()

        subproceso2.stdin.write(str(canalization) + str("\n"))
        subproceso2.stdin.flush()

        subproceso2.stdin.write(str(span_device) + str("\n"))
        subproceso2.stdin.flush()

        subproceso2.stdin.write(str(time_local) + str("\n"))
        subproceso2.stdin.flush()

        json_arreglo = subproceso2.stdout.readline()

        cadena = subproceso1.stdout.readline()

        print(cadena)

        subproceso1.stdin.write("terminar\n")
        subproceso1.stdin.flush()

        print("esperando confirmacion de parada")

        cadena = subproceso1.stdout.readline()

        print(cadena)

        cadena = subproceso1.stdout.readline()

        print(cadena)

        cadena = subproceso1.stdout.readline()

        print(cadena)

        print(json_arreglo)

        return str(json_arreglo)

    def protocolo(self):

        self.sock.send(self.tipoTarjeta)
        mensaje = str(self.sock.recv(self.tamano_paquetes))
        print ("Estado de la conexion: " + mensaje)
        self.sock.send("Escucho peticion")
        while True:
            mensaje = str(self.sock.recv(self.tamano_paquetes))
            print("llego la siguiente medicion: " + mensaje)
            self.sock.send("OK")
            if mensaje == "Ejecutar Medicion":
                mensaje = str(self.sock.recv(self.tamano_paquetes))
                arreglo = mensaje.split(";")

            if arreglo[0] == "occ":
                json_arreglo = self.correr_occupation(arreglo[1], arreglo[2], arreglo[3], arreglo[4], arreglo[5])
                print("Corriendo occ")
                self.grabar_samples_measurement(json_arreglo,"prueba_cliente")
                self.sock.send(json_arreglo)
        self.sock.close()

    def grabar_samples_measurement(self, resultado, measurement_id):
        file_name = str(measurement_id)
        with open("/home/andres/Escritorio/SimonController/modelo_cliente/results/" + file_name, "w") as outfile:
            json.dump(resultado, outfile)
            ##---------------------------------------------------------------------------------
            ##  Main
            ##---------------------------------------------------------------------------------


if __name__ == '__main__':
    #    os.chdir('/home/andres/Escritorio/Simon Controler')
    #    print(os.getcwd())
    mundo = Tarjeta_Cliente()
    # os.chdir('C:/Users/Andres/Dropbox/TRABAJO/i2t/Simon Controler/')
    # os.chdir('/home/andres/Escritorio/Simon Controler')
    mundo.protocolo()
