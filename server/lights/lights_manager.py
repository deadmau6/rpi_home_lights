from flask_socketio import SocketIO
from manager import Manager

class LightsManager(Manager):
    #This socket only acts as an emmiter.
    _socketio = SocketIO(message_queue='redis://', channel='lights')
    
    def update_event(self, data, pipe_fileno):
        """This is update data coming from the events"""
        if data['status'] == 'DONE':
            self.close_event(pipe_fileno)
        self._socketio.emit('status', data, broadcast=True)
        
