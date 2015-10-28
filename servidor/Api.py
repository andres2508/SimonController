import cherrypy
from modelo import Controlador


class Api(object):
    ##---------------------------------------------------------------------------------
    ##  Constructor
    ##---------------------------------------------------------------------------------

    def __init__(self):
        self.administrador = Controlador()
        self.p = None

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
