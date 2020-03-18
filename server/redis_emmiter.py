from flask_socketio import SocketIO
from time import sleep
import redis
import pickle
socketio = SocketIO(message_queue='redis://', channel='lights-request', http_compression=False)

def handle_lights(json):
    packet = pickle.loads(json['data'])
    print(packet['data']['message'])

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe(**{'lights-request': handle_lights})
    p.get_message()
    while True:
        try:
            p.get_message()
            usr_msg = input('-->')
            sleep(0.01)
        except KeyboardInterrupt:
            print('\nClosing Chat')
            break
        else:
            socketio.emit('status', {'message': usr_msg}, broadcast=True)
    p.close()
