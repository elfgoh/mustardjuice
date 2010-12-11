#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a handler for lighttpd+fastcgi
This file has to be in the PYTHONPATH
Put something like this in the lighttpd.conf file:

server.port = 8000
server.bind = '127.0.0.1'
server.event-handler = 'freebsd-kqueue'
server.modules = ('mod_rewrite', 'mod_fastcgi')
server.error-handler-404 = '/test.fcgi'
server.document-root = '/somewhere/web2py'
server.errorlog      = '/tmp/error.log'
fastcgi.server = ('.fcgi' =>
                    ('localhost' =>
                        ('min-procs' => 1,
                         'socket'    => '/tmp/fcgi.sock'
                        )
                    )
                 )
"""

LOGGING = False
SOFTCRON = False

import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

try:
    sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
except ValueError:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gluon.main
import gluon.contrib.gateways.fcgi as fcgi

if LOGGING:
    application = gluon.main.appfactory(wsgiapp=gluon.main.wsgibase,
                                        logfilename='httpserver.log',
                                        profilerfilename=None)
else:
    application = gluon.main.wsgibase

if SOFTCRON:
    from gluon.settings import global_settings
    global_settings.web2py_crontype = 'soft'

fcgi.WSGIServer(application, bindAddress='/tmp/fcgi.sock').run()