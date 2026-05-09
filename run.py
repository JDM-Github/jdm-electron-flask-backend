import os
from jdm_electron_flask import create_app, get_socketio

app = create_app()
socketio = get_socketio()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("FLASK_PORT", 5000)), debug=True)
