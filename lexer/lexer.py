import io
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

        while self.getCurrChar() == ' ' or self.getCurrChar() == '\n':
            self.getNextChar()

        position = self.getFilePosition()

        for try_to_build_token in [
                self.buildComment,
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
        print(f'unknown char {ord(self.getCurrChar())}')
        raise errors.LexerError("Unkown Token", file_handler=self.filehandler)

    def buildComment(self):
        if self.getCurrChar() == '#':
            while self.getNextChar() != '\n':
                pass
            else:
                self.getNextChar()

    def buildNumber(self):
        if not self.getCurrChar().isdecimal():
            return None
        collected_chars = [self.getCurrChar()]

        self.getNextChar()
        while self.getCurrChar().isdecimal():
            collected_chars.append(self.getCurrChar())
            self.getNextChar()
        if self.getCurrChar() == '.':
            collected_chars.append('.')
            self.getNextChar()
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

    def buildID(self):
        currChar = self.getCurrChar()
        if not (currChar.isalpha() or currChar == '_' or currChar == '$'):
            return None
        collected_chars = [currChar]

        self.getNextChar()
        while self.getCurrChar().isalnum() or self.getCurrChar() == '_':
            collected_chars.append(self.getCurrChar())
            self.getNextChar()

        result = ''.join(collected_chars)

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
