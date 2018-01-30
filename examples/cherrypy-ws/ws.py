import argparse
import configparser
import logging.config
import os

import cherrypy

# Config file directory
LOCAL_STORE = os.getcwd()
LOG_DIR = LOCAL_STORE + '/log/'

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

# Get parameters from config file
myconfigparser = configparser.ConfigParser()
CONFIG_FILEPATH = LOCAL_STORE + 'ws.config'
CONFIG_FILEPATH = '/home/hungap/development/python/cherrypy-ws/ws.config'
myconfigparser.read(CONFIG_FILEPATH)
appconfig = myconfigparser['APP']
AUTH_USERNAME = appconfig['username']
AUTH_PASSWORD = appconfig['password']

# Get customised settings from arguments
parser = argparse.ArgumentParser(description='Simple Cherrypy RESTful Web Service')
parser.add_argument('--basicAuthentication', action='store_true', help='Enable basic authentication', default=False)
parser.add_argument('--logLevel', default='INFO', help='Update log level, default level is INFO')
parser.add_argument('--ssl', action='store_true', help='Enable SSL', default=False)
args = parser.parse_args()
LOG_LEVEL = args.logLevel

if LOG_LEVEL == 'DEBUG':
    for key in appconfig: print(key + ":" + str(appconfig[key]))

LOG_CONF = {
    'version': 1,

    'formatters': {
        'void': {
            'format': ''
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'cherrypy_console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'void',
            'stream': 'ext://sys.stdout'
        },
        'cherrypy_access': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'void',
            'filename': LOG_DIR + 'cp_access.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'cp_main': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'void',
            'filename': LOG_DIR + 'cp_main.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL
        },
        'cherrypy.access': {
            'handlers': ['cherrypy_access'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'cherrypy.error': {
            'handlers': ['cherrypy_console', 'cp_main'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}
logging.config.dictConfig(LOG_CONF)


def validate_password(realm, username, password):
    return username == AUTH_USERNAME and password == AUTH_PASSWORD


@cherrypy.expose
class MyWebService:
    def GET(self, name):
        return 'Welcome ' + name + ', your GET request is successful'

    def POST(self, name):
        return 'Welcome ' + name + ', your POST request is successful'


if __name__ == '__main__':

    # Global config
    config = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80
    }

    if args.ssl:
        cherrypy.log('SSL enabled.')
        SSL_CERT = appconfig['username']
        SSL_KEY = appconfig['password']
        config['server.ssl_module'] = 'builtin'
        config['server.ssl_certificate'] = SSL_CERT
        config['server.ssl_private_key'] = SSL_KEY
        config['server.socket_port'] = 443
    cherrypy.config.update(config)

    ENABLE_AUTHENTICATION = args.basicAuthentication
    if ENABLE_AUTHENTICATION:
        if not AUTH_USERNAME or not AUTH_PASSWORD:
            cherrypy.log('WARNING: Must define realm, username and password in ' + CONFIG_FILEPATH
                         + ' to enable basic authentication.')
            ENABLE_AUTHENTICATION = False
        else:
            cherrypy.log('Basic Authentication enabled.')
    cherrypy.quickstart(MyWebService(), '/',
                        {
                            '/': {
                                'response.timeout': int(appconfig['response.timeout']),
                                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                                'tools.sessions.on': True,
                                'tools.response_headers.on': True,
                                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
                                'tools.auth_basic.on': ENABLE_AUTHENTICATION,
                                'tools.auth_basic.realm': 'myrealm',
                                'tools.auth_basic.checkpassword': validate_password
                            }
                        }
                        )
