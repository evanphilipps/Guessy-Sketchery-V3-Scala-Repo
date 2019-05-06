import json
import socket
from threading import Thread
from random import randint
from flask import Flask, send_from_directory, request, render_template
from flask_socketio import SocketIO

import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socket_server = SocketIO(app)

# ** Connect to Scala TCP socket server **
usernameToSid = {}
sidToUsername = {}

scala_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scala_socket.connect(('localhost', 8000))


def listen_to_scala(the_socket):
    delimiter = "~"
    buffer = ""
    while True:
        buffer += the_socket.recv(1024).decode()
        while delimiter in buffer:
            message = buffer[:buffer.find(delimiter)]
            buffer = buffer[buffer.find(delimiter) + 1:]
            get_from_scala(message)


Thread(target=listen_to_scala, args=(scala_socket,)).start()


def get_from_scala(data):
    message = json.loads(data)
    username = message["username"]
    user_socket = usernameToSid.get(username, None)
    if user_socket:
        socket_server.emit('message', data, room=user_socket)


def send_to_scala(data):
    scala_socket.sendall(json.dumps(data).encode())


# ** Setup and start Python web server **

@socket_server.on('connect')
def got_message(username):
    print(request.sid + " connected")
    usernameToSid[username] = request.sid
    sidToUsername[request.sid] = username
    message = {"username": username, "action": "connected"}
    send_to_scala(message)


@socket_server.on('disconnect')
def disconnect():
    print(request.sid + " disconnected")
    username = sidToUsername[request.sid]
    del sidToUsername[request.sid]
    del usernameToSid[username]
    message = {"username": sidToUsername[request.sid], "action": "disconnected"}
    send_to_scala(message)


# noinspection PyInterpreter
@socket_server.on('mouse')
def mouse_down():
    print(request.sid + " moused down")
    message = {"username": sidToUsername[request.sid], "action": "mouse"}
    send_to_scala(message)


@app.route('/')
def index():
    return send_from_directory('static_files', 'index.html')


@app.route('/game', methods=["POST", "GET"])
def game():
    if request.method == "POST":
        username = request.form.get('username')
    else:
        username = "GuestUser#" + str(randint(0, 100000))
    print(username + " registered")
    return render_template('game.html', username=username)


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('templates', filename)


print("Listening on port 8080")
socket_server.run(app, port=8080)
