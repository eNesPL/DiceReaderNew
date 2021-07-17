from wsgiref.simple_server import make_server

import falcon

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
from Config import Config


class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')


class GetDice:
    def on_get(self, req, resp):
        from DiceReader import readDice
        resp.status = falcon.HTTP_200
        resp.text = str(readDice())


class GetConnection:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = "connected"


global ui


def RestApiGetUi(d):
    global ui
    ui = d


# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
config = Config()
dice = GetDice()
connection = GetConnection()


# things will handle all requests to the '/things' URL path


def AddRoutes():
    app.add_route('/config', config)
    app.add_route('/getdice', dice)
    app.add_route('/getuseracrtion', ui)
    app.add_route('/getConnection', connection)


def RestApiServer():
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()

