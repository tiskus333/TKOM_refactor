from unittest.case import skip
from Lexer.filehandler import FileHandler
from Lexer.token import Token
import errors


class Lexer:
    def __init__(self, path_name: str, direct_input=False) -> None:
        self.reservedTokensDict = {'main': 0, 'class': 1, 'if': 2, 'else': 3, 'void': 4, 'float': 5, 'int': 6, 'return': 7, 'while': 8,  '(': 9, ')': 10,
                                   '{': 11, '}': 12, ':': 13, ';': 14, ',': 15, '.': 16,   '!': 17, '=': 18,  '+': 19, '-': 20, '<': 21, '>': 22, '==': 23, '!=': 24, '<=': 25, '>=': 26,  '#ID': 27,  "#INT_VAL": 28, "#FLOAT_VAL": 29, '#COM': 30, '#EOF': 31}
        self.TokenList = self.reservedTokensDict.keys()
        self.allowedafternumber = [
            ';', ',', '+', '-', '<', '>', '!', '<=', '>=', '==', '!=', '(', ')', '{', '}', '=', '.']
        self.filehandler = FileHandler(path_name, direct_input)
        self.__getNextChar()

    def __getNextChar(self):
        return self.filehandler.nextChar()

    def __getCurrChar(self):
        return self.filehandler.currChar()

    def __getFilePosition(self):
        return self.filehandler.getPosition()

    def buildToken(self, verbose=False) -> Token:

        while self.__getCurrChar().isspace():
            self.__getNextChar()

        position = self.__getFilePosition()

        for try_to_build_token in [
                self.__buildComment,
                self.__buildNumber,
                self.__buildID,
                self.__buildDoubleCharTokens,
                self.__buildSingleCharToken]:
            if token := try_to_build_token():
                token.position = position
                self.current_token = token
                if verbose:
                    print(token)
                return token

        # If not EOF -> unknown token
        if self.__getCurrChar():
            raise errors.LexerError(
                f"Unkown Token {ord(self.__getCurrChar()),self.__getCurrChar()}", file_handler=self.filehandler)
        else:
            return Token(type='#EOF', value='#EOF', position=position)

    # Try to build comment
    def __buildComment(self):
        if self.__getCurrChar() == '#':
            comment = ['#']
            while self.__getNextChar() != '\n' and self.__getCurrChar():
                comment.append(self.__getCurrChar())
            comment = ''.join(comment)
            return Token(type='#COM', value=comment)

    # Try tu build int or float number
    def __buildNumber(self):
        if not self.__getCurrChar().isdecimal():
            return None

        collected_chars = [self.__getCurrChar()]
        self.__getNextChar()

        # Add digit characters
        while self.__getCurrChar().isdecimal():
            collected_chars.append(self.__getCurrChar())
            self.__getNextChar()

        if not (self.__getCurrChar().isspace() or self.__getCurrChar() in self.allowedafternumber):
            raise errors.LexerError('Invalid token', self.filehandler)
        # Dot indicates float number
        if self.__getCurrChar() == '.':
            collected_chars.append('.')
            self.__getNextChar()
            if not self.__getCurrChar().isdecimal():
                raise errors.LexerError(
                    "Invalid number format, missing digit after dot", file_handler=self.filehandler)
            while self.__getCurrChar().isdecimal():
                collected_chars.append(self.__getCurrChar())
                self.__getNextChar()
            if not (self.__getCurrChar().isspace() or self.__getCurrChar() in self.allowedafternumber):
                raise errors.LexerError('Invalid token', self.filehandler)
            result = ''.join(collected_chars)
            return Token(
                type="#FLOAT_VAL",
                value=float(result)
            )
        else:
            result = ''.join(collected_chars)
            return Token(
                type="#INT_VAL",
                value=int(result)
            )

    # Try to build identificator or keyword
    def __buildID(self):
        currChar = self.__getCurrChar()
        if not (currChar.isalpha() or currChar in ['_', '$']):
            return None
        collected_chars = [currChar]

        self.__getNextChar()
        while self.__getCurrChar().isalnum() or self.__getCurrChar() in ['_', '$']:
            collected_chars.append(self.__getCurrChar())
            self.__getNextChar()

        result = ''.join(collected_chars)

        # Check if found word is a keyword, otherwise it is a new idenetificator
        token_type = result if result in self.TokenList else '#ID'

        return Token(
            type=token_type,
            value=result
        )

    def __buildDoubleCharTokens(self):
        char = self.__getCurrChar()
        if char in ['>', '<', '=', '!']:
            if (char2 := self.__getNextChar()) == '=':
                result = ''.join([char, char2])
                self.__getNextChar()
                return Token(
                    type=result,
                    value=result
                )
            else:
                return Token(
                    type=char,
                    value=char
                )
        else:
            return None

    def __buildSingleCharToken(self):
        char = self.__getCurrChar()
        if char in self.TokenList:
            self.__getNextChar()
            return Token(
                type=char,
                value=char
            )
        else:
            return None
