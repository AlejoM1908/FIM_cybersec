from tinydb import Query, TinyDB

from models.models import File, Log


class TinyDBManager:
    '''
        Class to manage TinyDB queries for data persistence
    '''
    def __init__(self, path:str):
        '''
            Class constructor

            @param {str} path - The path of the database
        '''
        self._connectDB(path)

    def _connectDB(self, path:str) -> None:
        '''
            Connect to the database

            @param {str} path - The path of the database
        '''
        self._db = TinyDB(path)
        self._files = self._db.table('files')
        self._logs = self._db.table('logs')

    def _dataFromJSON(self, data:dict) -> File | Log:
        '''
            Convert a data from JSON to File or Log

            @param {dict} data - The data to convert

            Returns a File or Log object
        '''
        if type(data['type']) == bool: return File(**data)
        else: return Log(**data)


    def _dataToJSON(self, data:File | Log) -> dict:
        '''
            Convert a data from File or Log to JSON

            @param {File | Log} data - The data to convert

            Returns a dict object
        '''
        return data.toDict()
    
    def getAll(self, *, is_file = True) -> list[File | Log]:
        '''
            Get all the data stored in the database

            Returns a list with the data stored in the database
        '''
        table = self._files if is_file else self._logs
        documents:list = table.all()

        for document in documents:
            document['id'] = document.doc_id

        return [self._dataFromJSON(document) for document in documents]
    
    def getOne(self, data_id:int, *, is_file = True) -> File | Log:
        '''
            Get the data with the given id

            @param {File | Log} type - The type of data to get
            @param {int} data_id - The id of the data to get

            Returns a dictionary with the data
        '''
        table = self._files if is_file else self._logs
        query:dict = table.get(doc_id=data_id)
        query['id'] = data_id
        return self._dataFromJSON(query)
    
    def getByParameter(self, parameter:str, value:str, *, is_file = True) -> list[File | Log]:
        '''
            Get the data that have the given parameter with the given value

            @param {File | Log} type - The type of data to get
            @param {str} parameter - The parameter to filter
            @param {str} value - The value to filter

            Returns a list with the data that match the filter
        '''
        query = Query()
        table = self._files if is_file else self._logs
        documents:list = table.search(query[parameter] == value)

        for document in documents:
            document['id'] = document.doc_id

        return [self._dataFromJSON(document) for document in documents]
    
    def saveData(self, data:File | Log, *, is_file = True) -> int:
        '''
            Save a new data in the database

            @param {File | Log} type - The type of data to save
            @param {File | Log} data - The data object to ve to saved

            Returns the id of the new data
        '''
        table = self._files if is_file else self._logs
        return table.insert(self._dataToJSON(data))
    
    def updateData(self, data:File | Log, *, is_file = True) -> None:
        '''
            Update a data in the database

            @param {File | Log} type - The type of data to update
            @param {File | Log} data - The data object to ve to updated
        '''
        table = self._files if is_file else self._logs
        table.update(self._dataToJSON(data), doc_ids=[data.id])

    def deleteData(self, data_id:int, *, is_file = True) -> None:
        '''
            Delete a data in the database

            @param {File | Log} type - The type of data to delete
            @param {int} data_id - The id of the data to delete
        '''
        table = self._files if is_file else self._logs
        table.remove(doc_ids=[data_id])