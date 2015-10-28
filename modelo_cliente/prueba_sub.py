import subprocess
import os
import time


os.chdir('/home/andres/Escritorio/Simon Controler/')
print(os.getcwd()+"Este es el directorio")

subproceso1 = subprocess.Popen("python /home/andres/Escritorio/Simon\ Controler/funciones/CubieBoard/bladeRF/Ocupacion/SIMONES_Occupation.py",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

time.sleep(20)

subproceso2 = subprocess.Popen("python /home/andres/Escritorio/Simon\ Controler/funciones/CubieBoard/bladeRF/Ocupacion/Fusion_Center_Occupation.py",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)


print("primer sleep")
time.sleep(10)
subproceso2.stdin.write("88000000" + '\n')
subproceso2.stdin.flush()

print("segundo sleep")
subproceso2.stdin.write(str("108000000") + str("\n"))
subproceso2.stdin.flush()

print("tercero sleep")
subproceso2.stdin.write(str("1000000") + str("\n"))
subproceso2.stdin.flush()

print("cuarto sleep")
subproceso2.stdin.write(str("20000000") + str("\n"))
subproceso2.stdin.flush()

print("esperando ACK")
cadena = subproceso2.stdout.readline()
print(cadena)
#cadena = subproceso2.stdout.readline()
#cadena = subproceso2.stdout.readline()

#time.sleep(5)
print("ultimo Sleep")
cadena = subproceso2.stdout.readline()

print("Esto es la cadena "+ cadena)

print("Esta corriendo")
