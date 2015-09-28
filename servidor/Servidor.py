from servidor import Api

__author__ = 'Andres'

import cherrypy

class Servidor(object):

    api = Api()

    def index(self):
        return "Hola Mundo!"
        index.exposed = True

    cherrypy.config.update({'server.socket_host':'192.168.160.95'})

if __name__=='__main__':
    cherrypy.quickstart(Servidor())