from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from src.colors.color import *


class LogType(Enum):
    ADDITION = "ADDITION"
    DELETION = "DELETION"
    MODIFICATION = "MODIFICATION"
    ALERT = "ALERT"

class FileType(Enum):
    FOLDER = 0
    FILE = 1

@dataclass(slots=True, kw_only=True)
class Log:
    id:Optional[int] = field(default=None)
    date:str
    type:LogType
    path:str

    def toDict(self) -> dict:
        '''
            Convert a Log object to a dict object
        '''
        return {
            'date': self.date,
            'type': self.type.value,
            'path': self.path
        }
    
    def setId(self, id:int) -> None:
        '''
            Set the id of the log
        '''
        self.id = id

    def __getitem__(self, item):
        '''
            Get the value of the given item
        '''
        return getattr(self, item)
    
    def __str__(self) -> str:
        '''
            Return a string representation of the Log object
        '''
        return f'{self.date} - {self.type.value} - {self.path}'

@dataclass(slots=True, kw_only=True)
class File:
    id:Optional[int] = field(default=None)
    name:str
    path:str
    type:str 

    def toDict(self) -> dict:
        '''
            Convert a File object to a dict object
        '''
        return {
            'name': self.name,
            'path': self.path,
            'type': self.type
        }
    
    def setId(self, id:int) -> None:
        '''
            Set the id of the file
        '''
        self.id = id

    def __getitem__(self, item):
        '''
            Get the value of the given item
        '''
        return getattr(self, item)
    
    def __str__(self) -> str:
        '''
            Return a string representation of the File object
        '''
        type_tag = f'{PURPLE if self.type == 1 else GREEN}({"Archivo" if self.type == 1 else "Directorio"}){WHITE}'
        return f'{self.name} - {type_tag}'