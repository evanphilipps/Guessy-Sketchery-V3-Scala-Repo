import json
import socket
from threading import Thread
from random import randint

from flask import Flask, send_from_directory, request, render_template
from flask_socketio import SocketIO

import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketServer = SocketIO(app)

usernameToSid = {}
sidToUsername = {}

js_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
js_socket.connect(('localhost', 8000))


def js_get(data):
    msg = json.loads(data)
    username = msg["username"]
    userSocket = usernameToSid.get(username, None)
    if userSocket:
        socketServer.emit('message', data, room=userSocket)


def js_listen(socket):
    delimiter = "~"
    buffer = ""
    while True:
        buffer += socket.recv(1024).decode()
        while delimiter in buffer:
            msg = buffer[:buffer.find(delimiter)]
            buffer = buffer[buffer.find(delimiter) + 1:]
            js_get(msg)


def js_send(data):
    js_socket.sendall(json.dumps(data).encode())


@socketServer.on('register')
def received_message(username):
    usernameToSid[username] = request.sid
    sidToUsername[request.sid] = username
    print(username + " connected")
    message = {"username": username, "action": "connected"}
    js_send(message)


@socketServer.on('disconnect')
def got_connection():
    if request.sid in sidToUsername:
        username = sidToUsername[request.sid]
        del sidToUsername[request.sid]
        del usernameToSid[username]
        print(username + " disconnected")
        message = {"username": username, "action": "disconnected"}
        js_send(message)

@app.route('/')
def login():
    return send_from_directory('static', 'login.html')


@app.route('/game', methods=["POST", "GET"])
def game():
    if request.method == "POST":
        username = request.form.get('username')
    else:
        username = "guest" + str(randint(0, 100000))
    return render_template('login.html', username=username)


socketServer.run(app, port=8080)