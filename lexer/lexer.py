from unittest.case import skip
from Lexer.filehandler import FileHandler
from Lexer.token import Token
import errors

reservedTokensDict = {'main': 0, 'class': 1, 'if': 2, 'else': 3, 'void': 4, 'float': 5, 'int': 6, 'while': 7, 'return': 8, '(': 9, ')': 10,
                      '{': 11, '}': 12, ':': 13, ';': 14, ',': 15, '.': 16,   '=': 17, '!': 18, '!=': 19, '==': 20, '<=': 21, '<': 22, '>': 23,  '>=': 24, '+': 25, '-': 26, '#ID': 27}


class Lexer:
    def __init__(self, path_name: str, direct_input=False) -> None:
        self.filehandler = FileHandler(path_name, direct_input)
        self.getNextChar()

    def getNextChar(self):
        return self.filehandler.nextChar()

    def getCurrChar(self):
        return self.filehandler.currChar()

    def getFilePosition(self):
        return self.filehandler.line, self.filehandler.position

    def buildToken(self, verbose=False):

        while self.getCurrChar().isspace() or self.skipComment():
            self.getNextChar()

        position = self.getFilePosition()

        for try_to_build_token in [
                self.buildNumber,
                self.buildID,
                self.buildDoubleCharTokens,
                self.buildSingleCharToken]:
            if token := try_to_build_token():
                token.position = position
                self.current_token = token
                if verbose:
                    print(token)
                return token

        # If not EOF -> unknown token
        if self.getCurrChar():
            raise errors.LexerError(
                f"Unkown Token {ord(self.getCurrChar())}", file_handler=self.filehandler)

    # Skip every character untill new line
    def skipComment(self):
        if self.getCurrChar() == '#':
            while self.getNextChar() != '\n':
                pass
            return True
        return False

    # Try tu build int or float number
    def buildNumber(self):
        if not self.getCurrChar().isdecimal():
            return None

        collected_chars = [self.getCurrChar()]
        self.getNextChar()

        # Add digit characters
        while self.getCurrChar().isdecimal():
            collected_chars.append(self.getCurrChar())
            self.getNextChar()

        # Dot indicates float number
        if self.getCurrChar() == '.':
            collected_chars.append('.')
            self.getNextChar()
            if not self.getCurrChar().isdecimal():
                raise errors.LexerError(
                    "Invalid number format, missing digit after dot", file_handler=self.filehandler)
            while self.getCurrChar().isdecimal():
                collected_chars.append(self.getCurrChar())
                self.getNextChar()

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
    def buildID(self):
        currChar = self.getCurrChar()
        if not (currChar.isalpha() or currChar in ['_', '$']):
            return None
        collected_chars = [currChar]

        self.getNextChar()
        while self.getCurrChar().isalnum() or self.getCurrChar() in ['_', '$']:
            collected_chars.append(self.getCurrChar())
            self.getNextChar()

        result = ''.join(collected_chars)

        # Check if found word is a keyword, otherwise it is a new idenetificator
        if not (token_type := reservedTokensDict.get(result)):
            token_type = reservedTokensDict["#ID"]

        return Token(
            type=token_type,
            value=result,
            position=(0, 0)
        )

    def buildDoubleCharTokens(self):
        char = self.getCurrChar()
        if char in ['>', '<', '=', '!']:
            if (char2 := self.getNextChar()) == '=':
                result = ''.join([char, char2])
                self.getNextChar()
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

    def buildSingleCharToken(self):
        char = self.getCurrChar()
        if char in reservedTokensDict:
            self.getNextChar()
            return Token(
                type=reservedTokensDict[char],
                value=char,
                position=(0, 0)
            )
        else:
            return None
