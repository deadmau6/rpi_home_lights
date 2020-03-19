from multiprocessing import Process, Pipe
from abc import ABC, abstractmethod
from light_event import LightEvent
import select, json, time

class Manager(ABC):
    """The Manager class

    This class is an event driven process manager.
    """

    def __init__(self):
        # Holds the total active events by id.
        self.active_events = {}
        # Holds the event connection for each dispatch pipe.
        self.active_pipes = {}
        # The event pipes are a one way connection from event to manager(updating).
        self.event_pipes = []
        # The dispatch pipes are a one way connection from manager to event(cancelling events).
        self.dispatch_pipes = []
        # TODO: boken pipes should contain both pipes and is only used for catching errors.
        self.broken_pipes = []

    @abstractmethod
    def update_event(self, data, pipe_fileno):
        pass

    def monitor(self):
        try:
            # This watches the currently active events for updates.
            readable, writable, errors = select.select(self.dispatch_pipes, self.event_pipes, self.event_pipes, 0.001)
            for conn in readable:
                self.read_event(conn)
        except Exception as e:
            self.close()
            raise e

    def register_event(self, conn, event_obj):
        """Registers a particular event based on the typ.

        Keyword arguments:
        conn -- connection to the manager(required by all events).
        event_obj --  arguments of the event(required by all events).      

        Returns the specified Event Instance (ie Searcher)
        """
        return LightEvent(conn, event_obj)

    def start_event(self, event_obj):
        """Starts the event."""
        event_id = event_obj['id']
        if event_id in self.active_events.keys():
            # This means that the same request was made twice in a row.
            print("Event already exists!")
        else:
            # Register and get the connection pipes between manager and event.
            parent_conn, child_conn = self.register_pipe()
            # Create an association between the manager pipe and event id.
            self.active_pipes[parent_conn.fileno()] = event_id
            # Get the specific event based on the type field.
            event = self.register_event(child_conn, event_obj)
            # The event needs to subclass Process from python's multiprocessing in order for this to work.
            event.start()
            # Create an association to the event id and all of it's connections/process objects.
            self.active_events[event_id] = (parent_conn, child_conn, event)
            # Log or print out the event created.
            print('Event PID: {0}'.format(event.pid))

    def read_event(self, conn):
        """Reads data sent from the spawned event through its pipe."""
        try:
            update_obj = conn.recv()
        except (EOFError, OSError) as ef:
            self.close_pipe(conn.fileno())
            # TODO: Custom errors!
            raise Exception(ef)
        else:
            self.update_event(update_obj, conn.fileno())

    def write_event(self, data, event_id):
        """Writes the Object data to the event given the event id."""
        if event_id in self.active_events.keys():
            parent_conn = self.active_events[event_id][0]
            try:
                parent_conn.send(data)
            except ValueError:
                print('Error: object to large could not be sent.')
            except Exception as e:
                print(e)
        else:
            print("Error: Event not found!")

    def cancel_event(self, event_id):
        """Sends a cancel message to the child event."""
        if event_id in self.active_events:
            parent_conn = self.active_events[event_id][0]
            parent_conn.send('abort')

    def register_pipe(self):
        """Add a pipe to the EventBus.

        Returns the dispatch's (or parent's) connection object
        and event's (or child's) connection object.
        """
        parent_conn, child_conn = Pipe() 
        self.dispatch_pipes.append(parent_conn)
        self.event_pipes.append(child_conn)
        return parent_conn, child_conn

    def close(self):
        """Safely close the entire manager and its children."""
        for pipe_fileno in self.active_pipes.keys():
                self.close_event(pipe_fileno)

    def close_event(self, pipe_fileno):
        """Safely closes an event and it's pipes.

        Keyword arguments:
        pipe_fileno -- should be a Connection Object's fileno which acts like a unique id

        In case the data comes back unreadable or just wrong we want to close the event at
        all cost. The pipe_fileno is the only guarentee for both broken and working pipes.
        """
        try:
            # The active_pipes should return the event id.
            event_id = self.active_pipes.pop(pipe_fileno)
            parent_conn, child_conn, event = self.active_events.pop(event_id)
            self.event_pipes.remove(child_conn)
            self.dispatch_pipes.remove(parent_conn)
        except KeyError as ke:
            print("The active pipe key does not exist.\n", ke)
        except ValueError as ve:
            print("Connection object does not exist.\n", ve)
        finally:
            # Close the connections.
            child_conn.close()
            parent_conn.close()
            # Kill the event, otherwise it will act a 'defunct' or a zombie on the OS.
            event.terminate()
            # Ensure that the event has terminated.
            event.join()
        