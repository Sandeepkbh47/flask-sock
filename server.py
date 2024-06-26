# from gevent.pywsgi import WSGIServer # Imports the WSGIServer
from gevent import monkey;
monkey.patch_all() 
import time
from flask import Flask,make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
# import socketio
# from aiohttp import web
# app = web.Application()

app=Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'
socketio=SocketIO(app, async_mode='gevent',cors_allowed_origins="*")

# sio = socketio.AsyncServer()
# sio.attach(app)
@socketio.on('message')
def message(data):
    print("data",data)

@app.route("/test")
def test():
    socketio.emit('message',{"count":100})
    return "Flask API"

def event_stream():
    count=1
    # while True:
    for i in range(20):
        yield 'data: %s\n\n' % {"count":count}
        count+=1
        time.sleep(0.3)

@app.route("/events")
def events():
        response=make_response(event_stream(),200)
        response.mimetype="text/event-stream"
        return response

@app.route("/")
def main():
    return "Flask development server"

# web.run_app(sio)
socketio.run(app,host='0.0.0.0',port=4000)
# LISTEN = ('0.0.0.0',4000)
# http_server = WSGIServer( LISTEN, app )
# http_server.serve_forever()
# app.run(host='0.0.0.0',port=4000)
##python C:\Users\belleza\AppData\Local\Programs\Python\Python311\Scripts\waitress-serve.exe --host 127.0.0.1 server:socketio