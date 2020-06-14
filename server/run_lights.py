from multiprocessing import freeze_support
from .lights import LightsManager
from time import sleep
import random
import redis
import pickle

"""
Event object format:
{
    id: number,
    status: string,
    mode: string,
    mode_params: dict,
}
"""

current_ID = random.randint(0, 10000)

lights = LightsManager()

lights.start_event({
    'id': current_ID,
    'status': 'running',
    'mode': 'SINGLE',
    'mode_params': { 'red': 255, 'blue': 0, 'green': 0}
})

print("Started Event: {0}".format({ 'id': current_ID, 'status': 'running', 'mode': 'SINGLE' }))

def handle_lights(json):
    packet = pickle.loads(json['data'])
    if packet['event'] == 'manager':
        lights.write_event(packet['data'], current_ID)

#if __name__ == "__main__":
if True:
    freeze_support()
    r = redis.Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe(**{'client': handle_lights})
    p.get_message()
    while True:
        try:
            p.get_message()
            lights.monitor()
            sleep(0.01)
        except KeyboardInterrupt:
            print('\nClosing...')
            lights.write_event({'status': 'shutdown'}, current_ID)
            break
        except Exception as e:
            print("\nClosing from error: {0}".format(e))
            lights.write_event({'status': 'shutdown'}, current_ID)
            break
    p.unsubscribe()
    p.close()
    lights.close()
    print("Lights Off.")
