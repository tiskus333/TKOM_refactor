import linecache
import re
from Lexer.token import Token


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
        pointer = re.sub('\S', ' ', line)
        pointer = pointer[:(column-1)] + '^' + pointer[column:]
        self.message = f'\nFile: "{file_name}", line {line_nr}, column {column}\nWhat: '\
            + description + f'\n{line}{pointer}'
        super().__init__(self.message)


class ParserError(Error):
    def __init__(self, message, curr_token) -> None:
        message += f'\nInstead got {curr_token}'
        super().__init__(message)
