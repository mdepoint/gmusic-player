import json
import subprocess
import time
from flask import Flask, request
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

pandora = None

class MusicPlayer(restful.Resource):

    def get(self):
        return "Hello"


    def post(self):
        global pandora

        info = request.get_json(force=True)

        if 'app' not in info:
            return 400

        if info['app']=='pandora':
            if pandora==None:
                print "Starting Pandora"
                pandora = subprocess.Popen( 'pianobar', stdin=subprocess.PIPE, stdout=subprocess.PIPE )
                print pandora
                time.sleep( 3 )
                pandora.stdin.write( '^' )
                time.sleep( 1 )
            
            if 'station' in info:
                pandora.stdin.write( 's' )
                time.sleep( 2 )

                stat = str(info['station']) + '\n'
                pandora.stdin.write( stat )
           
            if 'action' in info:
                if info['action']=='stop':
                    pandora.terminate()
                    pandora = None
                elif info['action']=='pause':
                    pandora.stdin.write( 'p' )





def init():
    api.add_resource(MusicPlayer, "/")

if __name__ == '__main__':
    init()


    app.run(host='0.0.0.0', port=8100)

