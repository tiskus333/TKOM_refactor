import linecache


class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class LexerError(Error):
    def __init__(self, description, file_handler) -> None:
        line_nr, column = file_handler.getPosition()
        file_name = file_handler.getFileName()
        if file_name == "STRING INPUT":
            line = file_handler.getStringLine(line_nr) + '\n'
        else:
            line = linecache.getline(file_name, line_nr)
        pointer = ''.join([' '*(column-1), '^'])
        self.message = f'\nFile: "{file_name}", line {line_nr}, column {column}\nWhat: '\
            + description + f'\n{line}{pointer}'
        super().__init__(self.message)
