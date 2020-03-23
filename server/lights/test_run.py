from multiprocessing import freeze_support
from .manager import Manager
import time
import argparse

"""
Event object format:
{
    id: number,
    status: string,
    mode: string,
    mode_params: dict,
}
"""

if __name__ == '__main__':
    freeze_support()

    id_num = 123

    parser = argparse.ArgumentParser(description='Parse user input')
    parser.add_argument('-s', '--status', type=str, help='Event Status', default='running')
    parser.add_argument('-m', '--mode', type=str, help='Lighting Mode', default='SINGLE')
    parser.add_argument('-p', '--params', type=str, help='Parameters for the lighting mode', default='{}')
    
    m = Manager()
    event = { 'id': id_num, 'status': 'running', 'mode': 'SINGLE' }
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
                args = parser.parse_known_args(usr_msg.split(' '))
                print(args)
                event['status'] = usr_msg
                m.write_event(event['id'], event)
            time.sleep(0.001)
            m.monitor()

