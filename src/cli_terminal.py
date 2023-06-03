import getpass
import os
import re

from .colors.color import *


class TerminalInterface:
    '''
        Used to generate general pourpose interactive terminal interfaces
    '''
    def __init__(self) -> None:
        self._static_messages = []
        self._current_location = os.getcwd()

    def _generateDivider(self, *, length:int = 35, char:str = '=') -> str:
        '''
            Generates a divider

            @param {int} length - The length of the divider
            @param {str} char - The char to use in the divider

            Returns the divider
        '''
        return char * length

    def _printStaticMessages (self) -> None:
        '''
            Prints all the static messages for the application
        '''
        for message in self._static_messages:
            print(f'{CYAN}... {WHITE}{message}')

        print(self._generateDivider())

    def _calculateTableWidth(self, list:list, matrix:list) -> list[int]:
        '''
            Calculate the max width of each index between the lists

            @param {list[str]} items - The list of items to calculate the width

            Returns a list with the width of each item
        '''
        #Check if every list has the same length
        if not all(len(item) == len(list) for item in matrix):
            raise ValueError('All lists must have the same length')
        
        #Calculate the max width of each index
        width = [len(str(item)) for item in list]
        for index, item in enumerate(list):
            max_row = max([len(str(row[index])) for row in matrix])
            if max_row > width[index]: width[index] = max_row

        return width

    def _printTableRows(self, items:list, *, widths:list = None, border_character:str = '|', middle_character:str = '|') -> None:
        '''
            Prints the rows of a table

            @param {list[str]} items - The list of items to print
            @param {str} border_character - The character to use for the start and end of the row (default: '|')
            @param {str} middle_character - The character to use every change of column (default: '|')
        '''
        if not widths: widths = [len(str(item)) for item in items]

        # if border = b, middle = m and data = d, the row must be printed like this: b d m d m d b
        print(f'{YELLOW}{border_character}', end='')
        for index, item in enumerate(items):
            print(f'{WHITE}{item}'.center(widths[index]), end='')
            if index < len(items) - 1: print(f'{YELLOW}{middle_character}', end='')
        print(f'{YELLOW}{border_character}{WHITE}')

    def _clearTerminal(self, *, print_static:bool = False) -> None:
        '''
            Clears the terminal and reprint the static messages if print_static is True

            @param {bool} print_static - Whether to reprint the static messages (default: False)
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

        if print_static: self._printStaticMessages()

    def printList(self, items:list[str], *, clear:bool = False, enumerate_options:bool = True, end:str = '\n') -> None:
        '''
            Just print a list of items, if enumerate is set to True, it will enumerate the items
            
            @param {list} items - The list of items to print
            @param {bool} clear - Whether to clear the terminal before printing the items (default: False)
            @param {bool} enumerate_options - Whether to enumerate the items (default: True)
            @param {str} end - The character to use when ending the print (default: '\n')
            
            Returns None
        '''
        if not items: return
        if clear: self._clearTerminal()

        for index, item in enumerate(items):
            print(f'{YELLOW}{index}. {WHITE}{item}' if enumerate_options else item, end=end)

    def intInput(self, input_msg:str, *, max:int = None, min:int = None, clear:bool = True, print_static:bool = False) -> str:
        '''
            Gets an integer input from the user
            If the user set a max or min value, the input must be between the range min < input <= max

            @param {str} input_msg - The message to display to the user
            @param {int} max - The maximum value the user can input (default: 0)
            @param {int} min - The minimum value the user can input (default: 0)
            @param {bool} clear - Whether to clear the terminal before displaying the message (default: True)
            @param {bool} print_static - Whether to add the message to the static messages array (default: False)

            Returns the user input if it's valid, throws a value error if it's invalid
        '''
        if max != None or min != None:
            if max == None: max = float('inf')
            if min == None: min = 0

            if max < min: raise ValueError('Max must be greater than min')

        if clear: self._clearTerminal(print_static=print_static)
        user_input = int(input(f'{YELLOW}?{CYAN} (int) {WHITE}{input_msg}'))

        if user_input < min or user_input > max: 
            raise ValueError('Invalid input')
        
        return user_input

    def booleanInput(self, input_msg:str, *, clear:bool = True, print_static:bool = False) -> bool:
        '''
            Gets a boolean input from the user

            @param {str} input_msg - The message to display to the user
            @param {str} error_msg - The message to display if the user input is invalid
            @param {bool} clear - Whether to clear the terminal before displaying the message (default: True)
            @param {bool} print_static - Whether to add the message to the static messages array (default: False)

            Returns the user input if it's valid, throws a value error if it's invalid
        '''
        if clear: self._clearTerminal(print_static=print_static)
        user_input = input(f'{YELLOW}?{CYAN} (yes/no) {WHITE}{input_msg}').lower()

        if user_input not in ['y', 'yes', 'n', 'no']:
            raise ValueError('Invalid input')
        
        return user_input in ['y', 'yes']

    def stringInput(self, input_msg:str, *, clear:bool = True, print_static:bool = False, safe:bool = False, correct:bool = False, hidden:bool = False) -> str:
        '''
            Gets a string input from the user, it only can contain letters, numbers, spaces and the following special characters: . , - _ @

            @param {str} input_msg - The message to display to the user
            @param {bool} clear - Whether to clear the terminal before displaying the message (default: True)
            @param {bool} print_static - Whether to add the message to the static messages array (default: False)
            @param {bool} safe - Whether to check the input for invalid characters (default: False)
            @param {bool} correct - Whether to correct the input if it contains invalid characters, if set to True it ignore the safe flag (default: False)

            Returns the user input if it's valid, throws a value error if it's invalid
        '''
        if clear: self._clearTerminal(print_static=print_static)
        user_input = input(f'{YELLOW}?{CYAN} (string) {WHITE}{input_msg}') if not hidden else getpass.getpass(f'{YELLOW}?{CYAN} (string) {WHITE}{input_msg}')

        # Checking for invalid characters, avoid innecesary checks if safe or correct is set to False
        if safe or correct:
            check:str = r'[^a-zA-Z0-9\s]+' # Regex to check for invalid characters substracting alphanumeric characters and spaces

            if not correct and re.search(check, user_input) is not None:
                raise ValueError('Invalid input')
            
            if correct: user_input = re.sub(check, '', user_input)
        
        return user_input

    def generateMenu(self, text:str, options: list[str], *, returnable:bool = True, print_static:bool = False, clear:bool = True) -> int:
        '''
            Displays a menu to the user and returns the selected option
            if returnable is set to True, the option 0 will be reserved to return, so the options will be enumarated starting from 1

            @param {str} title - The title of the menu
            @param {list[str]} options - The options to display to the user
            @param {bool} returnable - Whether to add the option to return to the menu (default: True)
            @param {bool} print_static - Whether to reprint the static messages (default: False)
            @param {bool} clear - Whether to clear the terminal before displaying the menu (default: True)

            Returns the user selected option index, or -1 if the user selected return and returnable is set to True
        '''
        error:bool = False
        movement:int = returnable

        while True:
            if clear: self._clearTerminal(print_static=print_static)
            if error: 
                print(f'{RED}! {YELLOW}Opción invalida!{WHITE}\n')
                error = False
            
            print(text, end='\n\n')

            # Printing the options
            if returnable: 
                self.printList(['Volver'] + options)
            else:
                self.printList(options)

            # Getting the user selection among the options
            try:
                user_input = self.intInput("Seleccione una opción: ", max=len(options) - 1 + movement, clear=False)
            except ValueError:
                if not clear: raise ValueError('Invalid input')
                error = True
                continue

            return user_input - movement

    def matchStringArrays(self, *, source: list[str] = None, target: list[str] = None, prematch: list[str] = None, purge_empty:bool = True) -> dict[str, str]:
        '''
            Displays a menu to the user to map a column of options to another
            
            @param {list[str]} source - The columns of the source list (default: None)
            @param {list[str]} target - The columns of the target list (default: None)
            @param {bool} purge_empty - Whether to remove empty values from the result map (default: True)
            
            Returns a tuple with the source and target columns mapped
        '''
        if source is None or target is None: raise ValueError('Source and target must be set')
        elif not source or not target: raise ValueError('Source and target must not be empty')

        if prematch:
            if len(prematch) != len(source): raise ValueError('Prematch must have the same length as source')
            result_map = {source[i]:prematch[i] for i in range(len(source))}
        else: 
            result_map = {source[i]:'' for i in range(len(source))}

        while True:
            options:list[str] = []

            # Display the result map so the user can see the mapping progress
            for key, value in result_map.items():
                options.append(f'{key} -> {value if value != "" else "Empty"}')

            # Choose a column from the source file to map
            user_input = self.generateMenu('Mapee todas las columnas que desee usar: \n', options)
            if user_input == -1: break

            # Choose a column from the target file to map to the selected source column
            map_input = self.generateMenu(f'Mapee la columna {source[user_input - 1]}', target)
            if map_input == -1: continue

            result_map[source[user_input]] = target[map_input]

        # Remove the empty values from the result map and return it

        if not purge_empty: 
            if '' in result_map.values(): raise ValueError('There are empty values in the result map')
            return result_map
        

        return {key:value for key, value in result_map.items() if value != ''}

    def editableList(self, message:str, array:list = None) -> list:
        '''
            Displays a menu to the user to edit a list of options

            @param {list} array - The array to edit (default: None)

            Returns the edited array
        '''
        if array is None: array = []
        error:bool = False

        while True:
            self._clearTerminal()
            options:list = ['Agregar elemento', 'Eliminar elemento', 'Finalizar edición']

            # Display the current array
            if error:
                print(f'{RED}!! {YELLOW}Opción invalida!{WHITE}\n')
                error = False
            self.print(message)
            self.printList(array, enumerate_options=False)

            # Get the user selection
            try:
                user_input = self.generateMenu('\n\nQue desea hacer con la lista?: ', options, returnable=False, clear=False)
            except ValueError:
                continue

            # Add an element to the array
            if user_input == 0:
                element:str = self.stringInput('Ingrese el elemento a agregar: ', clear=False)
                array.append(element)

            # Remove an element from the array
            elif user_input == 1:
                delete_index:int = self.generateMenu('\nQue elemento desea eliminar?: ', array, returnable=False)
                array.pop(delete_index)

            elif user_input == 2: break

        return array

    def insertPassword(self, message:str, *, min_length:int = 8, max_length:int = None, confirm:bool = True) -> str:
        '''
            Inserts a password from the user

            @param {str} message - The message to display to the user
            @param {int} min_length - The minimum length of the password (default: 8)
            @param {int} max_length - The maximum length of the password (default: None)
            @param {bool} confirm - Whether to ask the user to confirm the password (default: True)

            Returns the inserted password
        '''

        while True:
            password:str = self.stringInput(message, clear=False, hidden=True)

            # Check the password length
            if len(password) < min_length:
                self.print(f'{RED}! {YELLOW}La contraseña debe tener al menos {min_length} caracteres{WHITE}')
                continue
            elif max_length and len(password) > max_length:
                self.print(f'{RED}! {YELLOW}La contraseña debe tener menos de {max_length} caracteres{WHITE}')
                continue

            # Confirm the password if needed
            if confirm:
                confirm_password:str = self.stringInput('Confirme la contraseña: ', clear=False, hidden=True)
                if confirm_password != password:
                    self.print(f'{RED}! {YELLOW}Las contraseñas no coinciden{WHITE}')
                    continue

            return password

    def editableMap(self, map:dict = None) -> dict:
        '''
            Displays a menu to the user to edit a map of options

            @param {dict} map - The map to edit (default: None)

            Returns the edited map
        '''
        if map is None: map = {}

        while True:
            self._clearTerminal()
            options:list = ['Agregar elemento', 'Eliminar elemento', 'Finalizar edición']

            # Display the current map
            self.printList([f'{key} -> {value}' for key, value in map.items()], enumerate_options=False)

            # Get the user selection
            user_input = self.generateMenu('Que desea hacer con el mapa?: ', options)
            if user_input == 0: break

            # Add an element to the map
            elif user_input == 1:
                key:str = self.stringInput('Ingrese la clave del elemento a agregar: ')
                value:str = self.stringInput('Ingrese el valor del elemento a agregar: ')
                map[key] = value

            # Remove an element from the map
            elif user_input == 2:
                delete_index:int = self.generateMenu('Que elemento desea eliminar?: ', [f'{key} -> {value}' for key, value in map.items()])
                if delete_index != 0: del map[list(map.keys())[delete_index - 1]]

            elif user_input == 3: break

        return map

    def fileExplorer(self, *, text:str = None, extensions:str = None, only_directories:bool = False, print_static:bool = False) -> list:
        '''
            Generate a file system explorer, if a file is selected the path of the file is returned automatically, else wait for the user to select a directory manually
            The explorer add two options to the menu that all always first and second: 0 end the search and return the selected directory, 1 return to the parent directory
            When a path is a directory an slash is added at the end of the path name

            @param {str} text - The text to display at the top of the menu (default: None)
            @param {list[str]} extensions - The extensions of the files to show (default: None)
            @param {bool} only_directories - Whether to show only directories (default: False)
            @param {bool} print_static - Whether to print the menu staticly (default: False)

            Returns the path of the directory or file selected by the user, and a number indicating if the selected path is a directory (0) or a file (1)
        '''
        location:str = [self._current_location, 0]
        if extensions is None: extensions:list = []

        while True:
            self._clearTerminal()
            options:list = ['Finalizar selección', 'Ir al directorio anterior']

            # Get all the files and directories in the current path and place them in an matrix with 0 if is a directory or 1 if is a file [name, type]
            files:list = []
            for file in os.listdir(location[0]):
                full_path = os.path.join(location[0], file)
                file_type = 0 if os.path.isdir(full_path) else 1
                extension:str = os.path.splitext(file)[1] if file_type == 1 else None

                if only_directories and file_type == 1: continue
                if extensions and extension not in extensions and file_type == 1: continue

                files.append([file, file_type])
                options.append(f'{file} {f" - {GREEN}(Directorio)" if file_type == 0 else f" - {PURPLE}(Archivo)"}')

            user_input:int = self.generateMenu(f'{text}\nActualmente buscando en: {YELLOW}{location[0]}{WHITE}\n', options, returnable=False, print_static=print_static)

            # Static options: 0 end search, 1 parent directory
            if user_input == 0: 
                self._current_location = location[0]
                return location
            elif user_input == 1: 
                location[0] = os.path.dirname(location[0])
                continue

            if files[user_input - 2][1] == 1: 
                self._current_location = location[0]
                return [os.path.join(location[0], files[user_input - 2][0]), 1]
            
            location[0] = os.path.join(location[0], files[user_input - 2][0])

    def printTable(self, table:list, *, headers:list = None, print_static:bool = False, rows_per_page:int = 20) -> None:
        '''
            Print a matrix to the terminal in a pretty way adding a page system every 20 rows

            @param {list[list[str]]} table - The table to print
            @param {list[str]} headers - The headers of the table (default: None)
            @param {bool} print_static - Whether to print the table staticly (default: False)
            @param {int} rows_per_page - The number of rows to print per page (default: 20)

            Raises an error if the table is empty
        '''
        if not table: raise ValueError('The table cannot be empty')

        # Set headers from the first row of the table if not provided
        final_table:list = table.copy()
        if headers is None: 
            headers:list = final_table[0]
            final_table = final_table[1:]

        selected_page = 1
        error = False

        page_number = len(table) // rows_per_page + 1
        divided_table:list = [final_table[i:i + rows_per_page] for i in range(0, len(final_table), rows_per_page)]

        while True:
            # Calculate each column width
            widths:list = self._calculateTableWidth(headers, divided_table[selected_page - 1])

            self._clearTerminal(print_static=print_static)
            if error: 
                print(f'{RED}! {YELLOW}Opción invalida!{WHITE}\n')
                error = False
            print(f'Pagina {YELLOW}{selected_page} de {WHITE}{page_number}\n')

            # Print the headers
            self._printTableRows(headers, widths=widths)

            # Print separator
            self._printTableRows(['-' * width for width in widths], widths=widths, middle_character='+')

            # Print the data
            for row in divided_table[selected_page - 1]:
                self._printTableRows(row, widths=widths)

            # Add interactive options
            options:list = []
            if selected_page != 1: options.append('Pagina anterior')
            if selected_page != page_number: options.append('Pagina siguiente')
            options.append('Finalizar')

            try:
                user_input:int = self.generateMenu('\n', options, returnable=False, clear=False, print_static=print_static)
            except ValueError:
                error = True
                continue

            # Page selection logic
            if len(options) == 3:
                if user_input == 0: selected_page -= 1
                elif user_input == 1: selected_page += 1
                else: break

            elif len(options) == 2:
                if selected_page == 1 and user_input == 0: selected_page += 1
                elif selected_page == page_number and user_input == 0: selected_page -= 1
                else: break

            elif len(options) == 1 and user_input == 0: break
            else : error = True

    def multiselect(self, text:str, options:list, *, print_static:bool = False) -> list:
        '''
            Generate a multiselect menu

            @param {str} text - The text to display at the top of the menu
            @param {list[str]} options - The options to display
            @param {bool} print_static - Whether to print the menu staticly (default: False)

            Returns a list of the selected options
        '''
        selected_options:list = [False for _ in range(len(options))]
        error:bool = False

        while True:
            self._clearTerminal(print_static=print_static)
            if error: 
                print(f'{RED}! {YELLOW}Opción invalida!{WHITE}\n')
                error = False
            print(f'{text}\n\n', f'{YELLOW}0. {WHITE}Finalizar', sep='')

            for index, option in enumerate(options):
                print(f'{YELLOW}{index + 1}.[{GREEN}{"X" if selected_options[index] else " "}{YELLOW}] {WHITE}{option}')

            try:
                user_input:int = self.intInput('Escoja los indices que desea seleccionar: ', max=len(options), clear= False, print_static=print_static)
                if user_input == 0: break
                selected_options[user_input - 1] = not selected_options[user_input - 1]
            except ValueError:
                error = True
                continue

        return [options[index] for index, option in enumerate(selected_options) if option]

    def print(self, text:str, *, static:bool = False) -> None:
        '''
            Print a message to the terminal

            @param {str} text - The message to print
            @param {bool} static - Whether to print the message staticly (default: False)
        '''
        if static: 
            self._static_messages.append(text)
            print(f'{CYAN}... {WHITE}{text}')
        else: print(text)            
