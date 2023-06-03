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
        
         # Log the modification
        print(f"Modified: {event.src_path}")
        

    def on_deleted(self, event) -> None:
        '''
        Method that is called when a file is deleted.
        '''
        print(f"Deleted: {event.src_path}")
        
        pass



def start_observer(path):
    '''
    This function is responsible for starting the observer.
    '''
    observer = Observer()
    event_handler = PathObserver(path)
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            # Keep the observer running
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Example usage
if __name__ == "__main__":
    path_to_watch = "/path/to/watch"
    start_observer(path_to_watch)
