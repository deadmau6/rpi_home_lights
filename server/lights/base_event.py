
class BaseEvent:
    """The BaseEvent class

    This class is a parent class as for the event types.
    Therefore this class should only be inherited!
    This class holds the basic communication with the manager.
    """

    def __init__(self, event_conn):
        # Connection to the manager.
        self.event_conn = event_conn
        self._is_cancelled = False

    def report(self, status_report):
        """Send an update to the manager."""
        self.event_conn.send(status_report)

    def finish(self, conclusion):
        """Conclusion message to the manager."""
        self.event_conn.send(conclusion)
        self.event_conn.close()

    def check_manager(self, timeout=0.1):
        if self.event_conn.poll(timeout):
            try:
                update_obj = self.event_conn.recv()
            except (EOFError, OSError) as e:
                return { status: 'error', message: e.message }
            return update_obj
        return None
