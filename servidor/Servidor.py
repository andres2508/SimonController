from servidor import Api

__author__ = 'Andres'

import cherrypy
import json

class Servidor(object):

    api = Api()

    def index(self):
        return "Hola Mundo!"
        index.exposed = True

    @cherrypy.expose
    def update(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        # do_something_with(body)
        return "Updated %r." % (body,)

    cherrypy.config.update({'server.socket_host':'192.168.160.95'})

if __name__=='__main__':
    cherrypy.quickstart(Servidor())