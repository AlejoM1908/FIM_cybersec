from tinydb import Query, TinyDB

from typing import Union
from models.models import File, Log, Signature


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

    def _xor(self, *args:bool) -> bool:
        '''
            non odd parity XOR operation

            @param {*args} args - The arguments to apply the XOR operation

            Returns a bool
        '''
        result:int = 0

        for arg in args[0]:
            if arg: result += 1

        return result == 1

    def _connectDB(self, path:str) -> None:
        '''
            Connect to the database

            @param {str} path - The path of the database
        '''
        tables:list = ['files', 'logs', 'signatures']
        self._db = TinyDB(path)
        self._tables= {table: self._db.table(table) for table in tables}

    def _dataFromJSON(self, data:dict) -> Union[File, Log, Signature]:
        '''
            Convert a data from JSON to File or Log

            @param {dict} data - The data to convert

            Returns a File or Log object
        '''
        if 'signature' in data:
            return Signature(**data)
        elif type(data['type']) == str:
            return Log(**data)
        else:
            return File(**data)

    def _dataToJSON(self, data:File | Log | Signature) -> dict:
        '''
            Convert a data from File or Log to JSON

            @param {File | Log | Signature} data - The data to convert to JSON format

            Returns a dict object
        '''
        return data.toDict()
    
    def getAll(self, *, is_file = False, is_log = False, is_signature = False) -> list[Union[File, Log, Signature]]:
        '''
            Get all the data stored in the database

            @param {bool} is_file - If the data to get is a file
            @param {bool} is_log - If the data to get is a log
            @param {bool} is_signature - If the data to get is a signature

            Returns a list with the data formated as File, Log or Signature objects
        '''
        if not self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures']

        documents:list = table.all()

        for document in documents:
            document['id'] = document.doc_id

        return [self._dataFromJSON(document) for document in documents]
    
    def getOne(self, data_id:int, *, is_file = False, is_log = False, is_signature = False) -> Union[File, Log, Signature]:
        '''
            Get the data with the given id

            @param {int} data_id - The id of the data to get
            @param {bool} is_file - If the data to get is a file
            @param {bool} is_log - If the data to get is a log
            @param {bool} is_signature - If the data to get is a signature

            Returns a dictionary with the data formated as File, Log or Signature objects
        '''
        if not self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures'] 

        query:dict = table.get(doc_id=data_id)
        query['id'] = data_id
        return self._dataFromJSON(query)
    
    def getByParameter(self, parameter:str, value:str, *, is_file = False, is_log = False, is_signature = False) -> list[Union[File, Log, Signature]]:
        '''
            Get the data that have the given parameter with the given value

            @param {str} parameter - The parameter to search
            @param {str} value - The value of the parameter to search
            @param {bool} is_file - If the data to get is a file
            @param {bool} is_log - If the data to get is a log
            @param {bool} is_signature - If the data to get is a signature

            Returns a list with the data formated as File, Log or Signature objects
        '''
        if not self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures']

        query = Query()
        documents:list = table.search(query[parameter] == value)

        for document in documents:
            document['id'] = document.doc_id

        return [self._dataFromJSON(document) for document in documents]
    
    def saveData(self, data:File | Log | Signature, *, is_file = False, is_log = False, is_signature = False) -> int:
        '''
            Save a new data in the database

            @param {File | Log | Signature} data - The data to save
            @param {bool} is_file - If the data to save is a file
            @param {bool} is_log - If the data to save is a log
            @param {bool} is_signature - If the data to save is a signature

            Returns the id of the data saved
        '''
        if not self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures']

        return table.insert(self._dataToJSON(data))

    def updateData(self, data:File | Log | Signature, *, is_file = False, is_log = False, is_signature = False) -> None:       
        '''
            Update a data in the database

            @param {File | Log | Signature} data - The data to update
            @param {bool} is_file - If the data to update is a file
            @param {bool} is_log - If the data to update is a log
            @param {bool} is_signature - If the data to update is a signature

            Returns the id of the data updated
        '''
        if not self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures']

        test = table.update(self._dataToJSON(data), doc_ids=[data.id])
        print(test)

    def deleteData(self, data_id:int, *, is_file = False, is_log = False, is_signature = False) -> None:
        '''
            Delete a data in the database

            @param {File | Log} type - The type of data to delete
            @param {int} data_id - The id of the data to delete
        '''
        if self._xor([is_file, is_log, is_signature]): return None

        if is_file: table = self._tables['files']
        elif is_log: table = self._tables['logs']
        elif is_signature: table = self._tables['signatures']
        
        table.remove(doc_ids=[data_id])