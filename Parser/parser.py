from Parser.tree import Node, printTree
from typing import Optional
from Lexer.token import Token
from errors import ParserError
from Lexer.lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        assert(lexer is not None)
        self.__lexer = lexer
        self.__curent_token: Optional[Token] = None
        self.CST = []
        self.__getNextToken()
        self.__parseClassDefinition()

    def __getNextToken(self) -> Token:
        self.__curent_token = self.__lexer.buildToken()
        return self.__curent_token

    def __parseProgram(self):
        pass

    def __parseClassDefinition(self):
        if self.__curent_token.type == 'class':
            classNode = Node(self.__curent_token, [])
            if self.__getNextToken().type == '#ID':
                classNode.children.append(Node(self.__curent_token, []))
            else:
                raise ParserError('Expecting ID after class',
                                  self.__curent_token)
            if self.__getNextToken().type == ':':
                classNode.children.append(Node(self.__curent_token, []))
                if self.__getNextToken().type == '#ID':
                    classNode.children.append(Node(self.__curent_token, []))
                    self.__getNextToken()
                else:
                    raise ParserError(
                        'Expecting ID after :', self.__curent_token)

            if self.__curent_token.type != '{':
                raise ParserError(
                    'Excpecting "{" after class', self.__curent_token)
            else:
                classNode.children.append(Node(self.__curent_token, []))
                while self.__getNextToken() != '}':
                    if innerNode := self.__parseDefineStatement():
                        classNode.children.append(innerNode)
                    elif innerNode := self.__parseFunctionDefinition():
                        classNode.children.append(innerNode)
                classNode.children.append(Node(self.__curent_token, []))

            self.CST.append(classNode)

    def __parseFunctionDefinition(self):
        pass

    def __parseParameters(self):
        pass

    def __parseArguments(self):
        pass

    def __parseStatementBlock(self):
        pass

    def __parseIfStatement(self):
        pass

    def __parseWhileStatement(self):
        pass

    def __parseReturnStatement(self):
        pass

    def __parseDefineStatement(self):
        pass

    def __parseAssignStatement(self):
        pass

    def __parseExpression(self):
        pass

    def __parseBaseExpression(self):
        pass

    def __parseParenthesesExpr(self):
        pass

    def __parseCondition(self):
        pass

    def __parseRelationCondition(self):
        pass

    def __parseBaseCondition(self):
        pass

    def __parseParenthesesCondition(self):
        pass

    def __parseType(self):
        if self.__curent_token.type in ['int', 'float', '#ID']:
            return Node(self.__curent_token, [])

    def __parseArithmeticNegationOp(self):
        if self.__curent_token.type == '-':
            return Node(self.__curent_token, [])

    def __parseLogicNegationOp(self):
        if self.__curent_token.type == '!':
            return Node(self.__curent_token, [])

    def __parseAssignmentOP(self):
        if self.__curent_token.type == '=':
            return Node(self.__curent_token, [])

    def __parseRelationOp(self):
        if self.__curent_token.type in ['<', '>', '<=', '=>', '!=', '==']:
            return Node(self.__curent_token, [])

    def __parseAdditiveOp(self):
        if self.__curent_token.type in ['-', '+']:
            return Node(self.__curent_token, [])

    def __parseFuncCall(self):
        pass
