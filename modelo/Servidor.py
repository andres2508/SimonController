import Api
import os
__author__ = 'Andres'

import cherrypy
import json

class Servidor(object):

    api = Api.Api()
    @cherrypy.expose
    def index(self):
        return "Hola Mundo!"

    @cherrypy.expose
    def update(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        # do_something_with(body)
	print(boby)
        return "Updated %r." % (body,)

    cherrypy.config.update({'server.socket_host':'192.168.160.96','server.socket_port':9999})

if __name__=='__main__':
#    print(os.getcwd())
#    os.chdir('/home/andres/Escritorio/Simon Controler')
    print(os.getcwd())
    cherrypy.quickstart(Servidor())
