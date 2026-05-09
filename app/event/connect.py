from flask_socketio import emit
from app import socketio


@socketio.on("connect")
def on_connect():
    emit("connected", {"message": "Socket connected"})


@socketio.on("disconnect")
def on_disconnect():
    pass


@socketio.on("ping_server")
def on_ping(data):
    emit("pong_client", {"echo": data})
