from multiprocessing import Process
from .base_event import BaseEvent
from .lights_controller import LightsController
import time

class LightEvent(BaseEvent, Process):

    def __init__(self, event_conn, event_obj):
        BaseEvent.__init__(self, event_conn)
        Process.__init__(self)
        self.event_id = event_obj['id']
        self.lights = LightsController(event_obj)

    def log(self, update_msg, status="OK"):
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
                if request.get('status') == 'shutdown':
                    self.done('Safely shutting down.')
                    break
                self.lights.update(request)
            self.lights.run()
            time.sleep(1)

