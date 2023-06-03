from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class PathObserver(FileSystemEventHandler):
    '''
    PathObserver is a class that observes the changes to the given paths in track.
    '''
    def __init__(self, paths:str) -> None:
        '''
        Constructor for PathObserver class.
        '''
        self.paths = paths

    def on_modified(self, event:FileSystemEventHandler) -> None:
        '''
        Method that is called when a file is modified.
        '''
        if event.is_directory:
            return None
        
        

    def on_deleted(self, event) -> None:
        '''
        Method that is called when a file is deleted.
        '''
        pass



def start_observer(path:str) -> None:
    '''
    This function is responsible for starting the observer.
    '''
    observer = Observer()
    event_handler = PathObserver(path)
