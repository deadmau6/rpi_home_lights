from multiprocessing import freeze_support
from manager import Manager
import time

if __name__ == '__main__':
    freeze_support()
    
    m = Manager()
    event = { 'id': 123, 'status': 'running', 'mode': 'SINGLE' }
    m.start_event(event)
    print("Ctrl-C to end the process:")
    while True:
        try:
            usr_msg = input('-->')
        except KeyboardInterrupt:
            event['status'] = 'shutdown'
            m.write_event(event['id'], event)
            m.monitor()
            break
        else:
            if usr_msg:
                event['status'] = usr_msg
                m.write_event(event['id'], event)
            time.sleep(0.001)
            m.monitor()

