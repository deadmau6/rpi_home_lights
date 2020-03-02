import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pi_boi'
socketio = SocketIO(app, cors_allowed_origins='*', message_queue='redis://')

@socketio.on('lights')
def handle_lights(json):
	emit('status', json, broadcast=True)

if __name__ == '__main__':
	socketio.run(app, debug=True, host='0.0.0.0', port=4000)

