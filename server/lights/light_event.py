from multiprocessing import Process
from .base_event import BaseEvent
import time

class LightEvent(BaseEvent, Process):

	def __init__(self, event_conn, event_obj):
		BaseEvent.__init__(self, event_conn)
		Process.__init__(self)
