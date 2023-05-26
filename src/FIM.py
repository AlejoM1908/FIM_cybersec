from . cli_terminal import TerminalInterface
from . tinydb_controller import TinyDBManager
from models.models import File, Log
import os
from dotenv import dotenv_values

class FIM():
    def __init__(self):
        if not os.path.exists(f'{os.getcwd()}/.env'):
            with open('.env', 'w') as f:
                f.write('')

        self._interface = TerminalInterface()
        self._env = dotenv_values('.env')

    def _saveEnv(self, env_name:str,  value:str) -> None:
        '''
            Save a new environment variable to the .env file
        '''
        self._env[env_name] = value

        with open('.env', 'w') as f:
            for key, value in self._env.items():
                f.write(f'{key}={value}\n')

    def _getDBPath(self, message:str) -> None:
        '''
            Defines the path of the database
        '''
        options:list = ['Usar este directorio', 'Especificar directorio']
        path:str = ''

        option = self._interface.generateMenu(message, options, returnable=False)

        if option == 0:
            path = os.getcwd()
        elif option == 1:
            path = self._interface.fileExplorer(only_directories=True)[0]
            
        self._saveEnv('DB_PATH', f'{path}/.mapping.json')

    def _connectDB(self) -> None:
        '''
            Connect to the database

            @param {str} path - The path of the database
        '''
        path:str = ''

        if 'DB_PATH' not in self._env:
            self._getDBPath('No se encontró una base de datos, ¿Dónde desea crearla?')
            path = self._env['DB_PATH']
        else:
            path = self._env['DB_PATH']
        
        self._db = TinyDBManager(path)
        self._interface.print('Base de datos conectada correctamente', static=True)

    def _managePaths(self) -> None:
        '''
            Manage the paths that require to be managed
        '''
        paths:list = self._db.getAll()
        options:list = ['Agregar nueva ruta', 'Eliminar ruta', 'Regresar']
        
        while True:
            if len(paths) == 0:
                explorer = self._interface.fileExplorer(text='Seleccione una ruta')

                paths.append(File(name=os.path.basename(explorer[0]), path=explorer[0], type=explorer[1]))
                continue

            self._interface.printList(paths, clear=True, enumerate_options=False)
            option = self._interface.generateMenu('\nQue desea hacer?', options, clear=False, returnable=False)

            if option == 0:
                explorer = self._interface.fileExplorer(text='Seleccione una ruta')[0]
                
                path = File(name=os.path.basename(explorer), path=explorer, type=explorer[1])
                if path not in paths: paths.append(path)
                # ToDo: add the new file signature to the database

            elif option == 1:
                option = self._interface.generateMenu('Seleccione una ruta para eliminar', paths, returnable=False)
                paths.pop(option)
                # ToDo: remove the file signature from the database

            elif option == 2:
                self.paths = paths
                break

    def _checkIntegrity(self) -> None:
        '''
            Check the integrity of the files
        '''

        # ToDo: Load the file signatures from the database
        
        # Todo: Load the files paths to watchdog, if chages detected, generate a log and save it to the database


    def _mainMenu(self) -> None:
        '''
            Show the main menu
        '''
        options:list = ['Visualizar archivos/directorios en seguimiento', 'Comenzar seguimiento', 'Salir']
        option = self._interface.generateMenu('Menú principal', options, clear=False, returnable=False)

        while True:
            if option == 0:
                self._managePaths()
            elif option == 1:
                self._checkIntegrity()
            elif option == 2:
                self._interface.print('Saliendo del programa...', static=True)
                exit()

    def run(self) -> None:
        '''
            Run the program
        '''
        # Connect to the database
        self._connectDB()

        # Show the main menu
        self._mainMenu()