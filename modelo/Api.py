import cherrypy
import Controlador
import json
import time
import datetime


class Api(object):
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self):
        self.administrador = Controlador.Controlador()
        self.p = None
        self.administrador.protocolo_inicial()

    ##---------------------------------------------------------------------------------
    ##  Metodos
    ##---------------------------------------------------------------------------------

    @cherrypy.expose
    def index(self):
        return "Api Simon"

    @cherrypy.expose
    def correrblade(self, tiempo=60):
        t = float(tiempo)
        self.p = self.administrador.subproceso("python i2t_udp_synchronization_power_bladeRF.py", t)
        return "Esta corriendo blade!"

    @cherrypy.expose
    def verificar_estado(self):
        resultado = "Ya termino"
        if self.p.isAlive() == True:
            resultado = "Sigue Corriendo"
        return resultado

    @cherrypy.expose
    def terminar_proceso(self):
        respuesta = self.administrador.terminar_proceso()
        return respuesta

    @cherrypy.expose
    def measurement(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        # do_something_with(body)
        print("antes de enviar resultado")
        resultado = self.administrador.correr_funcion(0, body['measurement_type'], body['start_freq'],
                                                      body['final_freq'], body['canalization'], body['span_device'],
                                                      body['time'], body['samples'], body['id'])
        print((resultado))

        return (resultado)

    @cherrypy.expose
    def measurement_example(self, funcion, start_frec, final_frec, canalization, span_device, time, samples, id):
        resultado1 = self.administrador.correr_funcion(0, funcion, start_frec, final_frec, canalization, span_device,
                                                       time, 2, id)
        print "termino de correr medicion"
        resultado = json.loads(resultado1)
        name_measurement = resultado['name_measurement']
        umbral = resultado['umbral']
        scheduled_date = resultado['scheduled_date']
        date = datetime.datetime.fromtimestamp(scheduled_date).strftime('%Y-%m-%d %H:%M:%S')
        occupation = resultado['channel_occupation']
        channel_occupation = str(occupation).strip('[]')
        print(name_measurement, umbral, channel_occupation)
        # duration = resultado[15]+30
        return (
        "<html><head><title>Controlador Simon</title></head><body><h1>Resultados Medicion</h1><table><tr><td><strong>Campo</strong></td><td><strong>Resultado</strong></td></tr>"
        + "<tr><td>name_measurement  </td><td>" + name_measurement + "</td></tr>"
        + "<tr><td>start freq  </td><td>" + start_frec + "</td></tr>"
        + "<tr><td>final freq  </td><td>" + final_frec + "</td></tr>"
        + "<tr><td>canalization  </td><td>" + canalization + "</td></tr>"
        + "<tr><td>umbral  </td><td>" + str(umbral) + "</td></tr>"
        + "<tr><td>Channel Occupation  </td><td>" + channel_occupation + "</td></tr>"
        + "<tr><td>Scheduled  </td><td>" + date + "</td></tr>"
        + "</table></body></html>")

    @cherrypy.expose
    def prueba_url(self):
        return (
        "<html><head><title>Ejemplo de tabla sencilla</title></head><body><h1>Listado de cursos</h1><table><tr><td><strong>Curso</strong></td><td><strong>Horas</strong></td><td><strong>Horario</strong></td></tr>"
        + "<tr><td>CSS</td><td>20</td><td>16:00 - 20:00</td></tr></table></body></html>")
