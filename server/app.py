from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pi_boi'
socketio = SocketIO(app, message_queue='redis://')

@socketio.on('lights')
def handle_lights(json):
	emit('status', json, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)