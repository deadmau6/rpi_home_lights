from multiprocessing import Process
from .base_event import BaseEvent
from ..modes import LightModes
from time import sleep

class LightEvent(BaseEvent, Process):

    def __init__(self, event_conn, event_obj):
        BaseEvent.__init__(self, event_conn)
        Process.__init__(self)
        self.event_id = event_obj['id']
        self.lights = LightModes(event_obj)

    def log(self, update, status="OK"):
        self.report({
                'id': self.event_id,
                'update': update,
                'status': status,
            })

    def done(self, conclude_msg, status="DONE"):
        self.finish(conclusion={
                'id': self.event_id,
                'update': conclude_msg,
                'status': status,
            })
        
    def run(self):
        while True:
            request = self.check_manager()
            if request:
                if request.get('status') == 'error':
                    self.done(request.get('message'), 'ERROR')
                    break
                elif request.get('status') == 'shutdown':
                    self.done('Safely shutting down.')
                    break
                else:
                    update_obj = self.lights.update(request)
                    self.log(update_obj)
            self.lights.run()
            sleep(0.001)

