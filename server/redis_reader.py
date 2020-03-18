from time import sleep
import redis
import pickle

def handle_lights(json):
    packet = pickle.loads(json['data'])
    print(packet['data']['message'])

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe(**{'lights-request': handle_lights})
    p.get_message()
    print("Current Chat:")
    while True:
        try:
            p.get_message()
            sleep(0.01)
        except KeyboardInterrupt:
            print('\nClosing Chat')
            break
        except Exception as e:
            print("\nClosing from error: {0}".format(e))
            break
    p.unsubscribe()
    p.close()
