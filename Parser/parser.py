from Parser.tree import *
from typing import Optional
from Lexer.token import Token
from errors import ParserError
from Lexer.lexer import Lexer
from Parser.statements import *


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        assert(lexer is not None)
        self.__lexer = lexer
        self.__curent_token: Optional[Token] = None
        self.AST = []

        self.__parseProgram()

    def __getNextToken(self) -> Token:
        self.__curent_token = self.__lexer.buildToken()
        return self.__curent_token

    def __parseProgram(self):
        self.__getNextToken()
        while self.__curent_token.type != '#EOF':
            if result := self.__parseClassDefinition():
                self.AST.append(result)
            if result := self.__parseDefinition():
                self.AST.append(result)

    def __parseClassDefinition(self):
        if self.__curent_token.type == 'class':
            class_name = base_class = None
            members = []
            if self.__getNextToken().type == '#ID':
                class_name = self.__curent_token.value
            else:
                raise ParserError('Expecting ID after class',
                                  self.__curent_token)
            if self.__getNextToken().type == ':':
                if self.__getNextToken().type == '#ID':
                    base_class = self.__curent_token.value
                    self.__getNextToken()
                else:
                    raise ParserError(
                        'Expecting ID after :', self.__curent_token)

            if self.__curent_token.type != '{':
                raise ParserError(
                    'Excpecting "{" after class name', self.__curent_token)
            else:
                self.__getNextToken()
                while self.__curent_token.type not in ['}', '#EOF']:
                    if result := self.__parseDefinition():
                        members.append(result)
                self.__getNextToken()
            return ClassDefine(
                class_name, base_class, members)

    def __parseDefinition(self):
        if type := self.__parseType():
            if self.__getNextToken().type in ['#ID', 'main']:
                name = self.__curent_token.value
            else:
                raise ParserError('Excpecting ID after type',
                                  self.__curent_token)
            if self.__getNextToken().type == '(':
                parameters = self.__parseParameters()
                functionBlock = self.__parseStatementBlock()
                return FunctionDefine(type, name, parameters, functionBlock)
            elif self.__curent_token.type == ';':
                if name == 'main':
                    raise ParserError(
                        'Variable cannot be named with reserved keyword', self.__curent_token)
                if type == 'void':
                    raise ParserError(
                        'Variable cannot be of type void', self.__curent_token)
                self.__getNextToken()
                return VariableDefine(type, name)
            else:
                raise ParserError(
                    'Excpecting ; after variable definiton', self.__curent_token)

    def __parseParameters(self):
        if self.__curent_token.type == '(':
            parameters = []
            while self.__getNextToken().type != ')':
                if len(parameters) > 0 and self.__curent_token.type == ',':
                    self.__getNextToken()
                if type := self.__parseType():
                    if self.__getNextToken().type == '#ID':
                        name = self.__curent_token.value
                        parameters.append(ParameterDefine(type, name))
                    else:
                        raise ParserError(
                            'Expecting ID after type', self.__curent_token)
                else:
                    raise ParserError(
                        'Expecting variable type', self.__curent_token)
            self.__getNextToken()
        return parameters

    def __parseArguments(self):
        pass

    def __parseStatementBlock(self):
        if self.__curent_token.type == '{':
            while self.__getNextToken().type != '}':
                pass
            self.__getNextToken()
        return []

    def __parseIfStatement(self):
        if self.__curent_token.type == 'if':
            if self.__getNextToken().type == '(':
                condition = self.__parseCondition()
                if self.__curent_token.type != ')':
                    raise ParserError(
                        "Expecting ) after condition", self.__curent_token)
                ifBlock = self.__parseStatementBlock()
                elseBlock = None
                if self.__curent_token.type == 'else':
                    elseBlock = self.__parseStatementBlock()
                return IfStatement(condition, ifBlock, elseBlock)
            else:
                raise ParserError(
                    "Expecting ( after if token", self.__curent_token)

    def __parseWhileStatement(self):
        if self.__curent_token.type == 'while':
            if self.__getNextToken().type == '(':
                condition = self.__parseCondition()
            else:
                raise ParserError(
                    'Expecting ( after while token', self.__curent_token)

    def __parseReturnStatement(self):
        if self.__curent_token.type == 'return':
            return_value, return_type = self.__parseExpression()
            if not return_value is None:
                return ReturnStatement(return_value, return_type)
            else:
                raise ParserError(
                    'Expecting return value after return keyword', self.__curent_token)
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
        if self.__curent_token.type in ['int', 'float', 'void', '#ID']:
            return self.__curent_token.value
        else:
            return None

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
