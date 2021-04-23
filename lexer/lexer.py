from unittest.case import skip
from Lexer.filehandler import FileHandler
from Lexer.token import Token
import errors

reservedTokensDict = {'main': 0, 'class': 1, 'if': 2, 'else': 3, 'void': 4, 'float': 5, 'int': 6, 'while': 7, 'return': 8, '(': 9, ')': 10,
                      '{': 11, '}': 12, ':': 13, ';': 14, ',': 15, '.': 16,   '=': 17, '!': 18, '!=': 19, '==': 20, '<=': 21, '<': 22, '>': 23,  '>=': 24, '+': 25, '-': 26, '#ID': 27}


class Lexer:
    def __init__(self, path_name: str, direct_input=False) -> None:
        self.filehandler = FileHandler(path_name, direct_input)
        self.__getNextChar()

    def __getNextChar(self):
        return self.filehandler.nextChar()

    def __getCurrChar(self):
        return self.filehandler.currChar()

    def __getFilePosition(self):
        return self.filehandler.getPosition()

    def buildToken(self, verbose=False) -> Token:

        while self.__getCurrChar().isspace() or self.__skipComment():
            self.__getNextChar()

        position = self.__getFilePosition()

        for try_to_build_token in [
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
                f"Unkown Token {ord(self.__getCurrChar())}", file_handler=self.filehandler)

    # Skip every character untill new line
    def __skipComment(self):
        if self.__getCurrChar() == '#':
            while self.__getNextChar() != '\n':
                pass
            return True
        return False

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

            result = ''.join(collected_chars)
            return Token(
                type=reservedTokensDict["float"],
                value=float(result),
                position=(0, 0)
            )
        else:
            result = ''.join(collected_chars)
            return Token(
                type=reservedTokensDict["int"],
                value=int(result),
                position=(0, 0)
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
        if not (token_type := reservedTokensDict.get(result)):
            token_type = reservedTokensDict["#ID"]

        return Token(
            type=token_type,
            value=result,
            position=(0, 0)
        )

    def __buildDoubleCharTokens(self):
        char = self.__getCurrChar()
        if char in ['>', '<', '=', '!']:
            if (char2 := self.__getNextChar()) == '=':
                result = ''.join([char, char2])
                self.__getNextChar()
                return Token(
                    type=reservedTokensDict[result],
                    value=result,
                    position=(0, 0)
                )
            else:
                return Token(
                    type=reservedTokensDict[char],
                    value=char,
                    position=(0, 0)
                )
        else:
            return None

    def __buildSingleCharToken(self):
        char = self.__getCurrChar()
        if char in reservedTokensDict:
            self.__getNextChar()
            return Token(
                type=reservedTokensDict[char],
                value=char,
                position=(0, 0)
            )
        else:
            return None
