from os import system


class Error(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class LexerError(Error):
    def __init__(self, description, file_handler) -> None:

        self.message = 'LEXER ERROR ' + description + \
            f' in file {file_handler.file_name}, at line {file_handler.line}, column {file_handler.position + 1}'
        super().__init__(self.message)
