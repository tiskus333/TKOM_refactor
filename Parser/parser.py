from typing import Optional
from Lexer.token import Token
from errors import ParserError
from Lexer.lexer import Lexer
from Parser.types import *


class Parser:
    def __init__(self, lexer: Lexer, tests=False) -> None:
        assert(lexer is not None)
        self.__lexer = lexer
        self.__current_token: Optional[Token] = None
        self.AST = []
        self.__getNextToken()
        if not tests:
            self.parseProgram()

    def __getNextToken(self) -> Token:
        self.__current_token = self.__lexer.buildToken()
        return self.__current_token

    def parseProgram(self):
        while result := self.parseAny([self.parseClassDefinition, self.parseDefinition]):
            self.AST.append(result)
            if isinstance(result, FunctionDefine) and self.__current_token.type == ';':
                raise ParserError(
                    'Unwanted ; after function definition', self.__current_token)
        if self.__current_token.type != '#EOF':
            raise ParserError(
                'Expecting class or function definition', self.__current_token)

    def parseClassDefinition(self):
        if self.__current_token.type == 'class':
            class_name = base_class = None
            members = []
            if self.__getNextToken().type == '#ID':
                class_name = self.__current_token.value
            else:
                raise ParserError('Expecting ID after class',
                                  self.__current_token)
            if self.__getNextToken().type == ':':
                if self.__getNextToken().type == '#ID':
                    base_class = self.__current_token.value
                    self.__getNextToken()
                else:
                    raise ParserError(
                        'Expecting ID after :', self.__current_token)

            if self.__current_token.type != '{':
                raise ParserError(
                    'Excpecting "{" after class name', self.__current_token)
            else:
                self.__getNextToken()
                while result := self.parseDefinition():
                    members.append(result)
                if self.__current_token.type != '}':
                    raise ParserError(
                        'Excpecting } after class body', self.__current_token)
                if self.__getNextToken().type != ';':
                    raise ParserError(
                        'Expecting ; after class definition', self.__current_token)
                self.__getNextToken()
            return ClassDefine(
                class_name, base_class, members)

    def parseDefinition(self, type=None):
        if type is None:
            type = self.parseType()
        if type:
            if self.__current_token.type in ['#ID', 'main']:
                name = self.__current_token.value
            elif self.__current_token.type == '=':
                return self.parseVariableAccess(type)
            elif self.__current_token.type == '(':
                raise ParserError('Expecting ID after type',
                                  self.__current_token)
            elif self.__current_token.value in self.__lexer.TokenList:
                raise ParserError(
                    'Variable cannot be named with reserved keyword', self.__current_token)
            if self.__getNextToken().type == '(':
                parameters = self.parseParameters()
                functionBlock = self.parseStatementBlock()
                if functionBlock:
                    return FunctionDefine(type, name, parameters, functionBlock)
                else:
                    raise ParserError(
                        'Incorrect function definition', self.__current_token)
            elif self.__current_token.type == ';':
                if type == 'void':
                    raise ParserError(
                        'Variable cannot be of type void', self.__current_token)
                self.__getNextToken()
                return VariableDefine(type, name)
            else:
                raise ParserError(
                    'Excpecting ; after variable definiton', self.__current_token)

    def parseFuncCall(self, name=None):
        if name is None:
            name = self.parseNestedName()
        if name and self.__current_token.type == '(':
            arguments = self.parseArguments()
            self.__getNextToken()
            return FuncCall(name, arguments)

    def parseVariableAccess(self, name=None):
        if name is None:
            name = self.parseNestedName()
        if name:
            if self.__current_token.type == '(':
                return self.parseFuncCall(name)
            if self.__current_token.type == '=':
                return self.parseAssignStatement(name)
            elif self.__current_token.type == '#ID' and len(name) == 1:
                return self.parseDefinition(name)
            else:
                return VariableAccess(name)

    def parseParameters(self):
        if self.__current_token.type == '(':
            parameters = []
            while self.__getNextToken().type != ')':
                if len(parameters) > 0 and self.__current_token.type == ',':
                    self.__getNextToken()
                if type := self.parseType():
                    if self.__current_token.type == '#ID':
                        name = self.__current_token.value
                        parameters.append(ParameterDefine(type, name))
                    else:
                        raise ParserError(
                            'Expecting ID after type', self.__current_token)
                elif self.__current_token.type != ')':
                    raise ParserError(
                        'Expecting ) after parameters', self.__current_token)
                else:
                    raise ParserError(
                        'Expecting variable type', self.__current_token)
            self.__getNextToken()
        return parameters

    def parseArguments(self):
        if self.__current_token.type == '(':
            arguments = []
            self.__getNextToken()
            while self.__current_token.type != ')':
                if len(arguments) > 0 and self.__current_token.type == ',':
                    self.__getNextToken()
                if result := self.parseExpression():
                    arguments.append(result)
                else:
                    raise ParserError(
                        'Expecting closing bracket after arguments', self.__current_token)
            return arguments

    def parseStatementBlock(self):
        if self.__current_token.type == '{':
            operations = []
            operation = None
            self.__getNextToken()
            while operation := self.parseAny([
                    self.parseIfStatement,
                    self.parseReturnStatement,
                    self.parseVariableAccess,
                    self.parseDefinition,
                    self.parseWhileStatement,
                    self.parseStatementBlock]):
                operations.append(operation)
                if isinstance(operation, FuncCall):
                    if self.__current_token.type != ';':
                        raise ParserError(
                            'Expecting ; after function call', self.__current_token)
                    else:
                        operation.standalone = True
                        self.__getNextToken()
            if self.__current_token.type == '}':
                self.__getNextToken()
            else:
                raise ParserError(
                    'Expecting } after statementBlock', self.__current_token)

            return StatementBlock(operations)

    def parseAny(self, functions):
        for f in functions:
            if result := f():
                return result

    def parseIfStatement(self):
        if self.__current_token.type == 'if':
            if self.__getNextToken().type == '(':
                self.__getNextToken()
                condition = self.parseCondition()
                if self.__current_token.type != ')':
                    raise ParserError(
                        "Expecting ) after condition", self.__current_token)
                self.__getNextToken()
                if ifBlock := self.parseStatementBlock():
                    elseBlock = None
                    if self.__current_token.type == 'else':
                        self.__getNextToken()
                        elseBlock = self.parseStatementBlock()
                    return IfStatement(condition, ifBlock, elseBlock)
                else:
                    raise ParserError(
                        'Expecting { after if condition', self.__current_token)
            else:
                raise ParserError(
                    "Expecting ( after if token", self.__current_token)

    def parseWhileStatement(self):
        if self.__current_token.type == 'while':
            if self.__getNextToken().type == '(':
                self.__getNextToken()
                condition = self.parseCondition()
                if self.__current_token.type != ')':
                    raise ParserError(
                        'Expecting ) after condition', self.__current_token)
                if self.__getNextToken().type != '{':
                    raise ParserError(
                        'Expecting { after while condition', self.__current_token)
                statementBlock = self.parseStatementBlock()
                return WhileStatement(condition, statementBlock)
            else:
                raise ParserError(
                    'Expecting ( after while token', self.__current_token)

    def parseReturnStatement(self):
        if self.__current_token.type == 'return':
            self.__getNextToken()
            return_value = self.parseExpression()
            if self.__current_token.type == ';':
                self.__getNextToken()
                return ReturnStatement(return_value)
            else:
                raise ParserError(
                    'Expecting ; after return value', self.__current_token)

    def parseAssignStatement(self, name=None):
        if name is None:
            name = self.parseNestedName()
        if self.parseAssignmentOP():
            if expression := self.parseExpression():
                if self.__current_token.type == ';':
                    self.__getNextToken()
                    return AssignStatement(VariableAccess(name), expression)
                else:
                    raise ParserError(
                        'Expecting ; after assignment operation', self.__current_token)
            else:
                raise ParserError(
                    'Expecting expression after assignment operator', self.__current_token)

    def parseExpression(self):
        lvalue = self.parseBaseExpression()
        if operator := self.parseAdditiveOp():
            if rvalue := self.parseExpression():
                return MathExpression(lvalue, operator, rvalue)
            else:
                raise ParserError(
                    'Expecting expression after operator', self.__current_token)
        else:
            return lvalue

    def parseBaseExpression(self):
        if negation := self.__current_token.type == '-':
            self.__getNextToken()
        for try_parse in [self.parseNumber,
                          self.parseParenthesesExpression,
                          self.parseVariableAccess, ]:
            if value := try_parse():
                break

        if negation:
            return Negation(value)
        if try_parse:
            if try_parse == self.parseNumber:
                return BaseExpression(value)
            else:
                return value

    def parseParenthesesExpression(self):
        if self.__current_token.type == '(':
            self.__getNextToken()
            expression = self.parseExpression()
            if self.__current_token.type == ')':
                self.__getNextToken()
                return ParenthesesExpression(expression)
            else:
                raise ParserError('Expecting ) after expression',
                                  self.__current_token)

    def parseCondition(self):
        lcond = self.parseBaseCondition()
        if operator := self.parseRelationOp():
            rcond = self.parseBaseCondition()
            return RelationCondition(lcond, operator, rcond)
        return lcond

    def parseBaseCondition(self):
        if self.parseLogicNegationOp():
            return LogicNegation(self.parseParenthesesCondition())
        else:
            return self.parseExpression()

    def parseParenthesesCondition(self):
        if self.__current_token.type == '(':
            self.__getNextToken()
            condition = self.parseCondition()
            if self.__current_token.type == ')':
                self.__getNextToken()
                return ParenthesesCondition(condition)
            else:
                raise ParserError('Expecting ) after condition',
                                  self.__current_token)
        else:
            raise ParserError('Expecting ( after !', self.__current_token)

    def parseNestedName(self):
        if self.__current_token.type == '.':
            raise ParserError('Expecting ID before .', self.__current_token)
        if self.__current_token.type == '#ID':
            nested_name = [self.__current_token.value]
            while self.__getNextToken().type == '.':
                if self.__getNextToken().type == '#ID':
                    nested_name.append(self.__current_token.value)
                else:
                    raise ParserError('Expecting ID after .',
                                      self.__current_token)
            return '.'.join(nested_name)

    def parseType(self):
        x = self.__current_token
        if x.type in ['int', 'float', 'void', '#ID']:
            self.__getNextToken()
            if self.__current_token.type != '.':
                return x.value

    def parseNumber(self):
        x = self.__current_token
        if x.type in ['#INT_VAL', '#FLOAT_VAL']:
            self.__getNextToken()
            return x.value

    def parseLogicNegationOp(self):
        x = self.__current_token
        if x.type == '!':
            self.__getNextToken()
            return x.value

    def parseAssignmentOP(self):
        x = self.__current_token
        if x.type == '=':
            self.__getNextToken()
            return x.type

    def parseRelationOp(self):
        x = self.__current_token
        if x.type in ['<', '>', '<=', '=>', '!=', '==']:
            self.__getNextToken()
            return x.value

    def parseAdditiveOp(self):
        x = self.__current_token
        if x.type in ['-', '+']:
            self.__getNextToken()
            return x.value
