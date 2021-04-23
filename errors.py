from os import system


class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class LexerError(Error):
    def __init__(self, description, file_handler) -> None:
        line, column = file_handler.getPosition()
        self.message = 'LEXER ERROR ' + description + \
            f' in file {file_handler.getFileName()}, at line {line}, column {column + 1}'
        super().__init__(self.message)
