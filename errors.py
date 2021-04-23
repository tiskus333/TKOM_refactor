import linecache


class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class LexerError(Error):
    def __init__(self, description, file_handler) -> None:
        line_nr, column = file_handler.getPosition()
        line = linecache.getline(file_handler.getFileName(), line_nr)
        pointer = ''.join([' '*(column-1), '^'])
        self.message = f'\nFile: "{file_handler.getFileName()}", line {line_nr}, column {column}\nWhat: '\
            + description + f'\n{line}{pointer}'
        super().__init__(self.message)
# dodać wyswietlenie linii
