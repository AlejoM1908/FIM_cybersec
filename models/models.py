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
        return f'{self.path} - {self.type.value} - {self.date}'
    
    def __eq__(self, other) -> bool:
        '''
            Compare two Log objects
        '''
        return self.date == other.date and self.type == other.type and self.path == other.path
    
    def __hash__(self) -> int:
        '''
            Return the hash of the Log object
        '''
        return hash((self.date, self.type, self.path))

@dataclass(slots=True, kw_only=True)
class File:
    id:Optional[int] = field(default=None)
    name:str
    path:str
    type:str
    signed:bool = field(default=False)

    def toDict(self) -> dict:
        '''
            Convert a File object to a dict object
        '''
        return {
            'name': self.name,
            'path': self.path,
            'type': self.type,
            'signed': self.signed
        }
    
    def setId(self, id:int) -> None:
        '''
            Set the id of the file
        '''
        self.id = id

    def shortStr(self) -> str:
        '''
            Return a short string representation of the File object
        '''
        type_tag = f'{PURPLE if self.type == 1 else GREEN}({"Archivo" if self.type == 1 else "Directorio"}){WHITE}'
        return f'{self.name} - {type_tag}'

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
        sign_tag = f'{RED if not self.signed else CYAN}({"No firmado" if not self.signed else "Firmado"}){WHITE}'
        return f'{self.name} - {type_tag} - {sign_tag}'
    
    def __eq__(self, other) -> bool:
        '''
            Compare two File objects
        '''
        return self.name == other.name and self.path == other.path and self.type == other.type and self.signed == other.signed
    
    def __hash__(self) -> int:
        '''
            Return the hash of the File object
        '''
        return hash((self.name, self.path, self.type, self.signed))

@dataclass(slots=True, kw_only=True)
class Signature:
    id:Optional[int] = field(default=None)
    signature:str
    date:str
    path:str

    def toDict(self) -> dict:
        '''
            Convert a Signature object to a dict object
        '''
        return {
            'signature': self.signature,
            'date': self.date,
            'path': self.path
        }
    
    def setId(self, id:int) -> None:
        '''
            Set the id of the signature
        '''
        self.id = id

    def __getitem__(self, item):
        '''
            Get the value of the given item
        '''
        return getattr(self, item)
    
    def __str__(self) -> str:
        '''
            Return a string representation of the Signature object
        '''
        return f'{self.path} - {self.date}'
    
    def __eq__(self, other) -> bool:
        '''
            Compare two Signature objects
        '''
        return self.signature == other.signature and self.date == other.date and self.path == other.path
    
    def __hash__(self) -> int:
        '''
            Return the hash of the Signature object
        '''
        return hash((self.signature, self.date, self.path))
