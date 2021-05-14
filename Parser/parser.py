from Parser.tree import *
from typing import Optional
from Lexer.token import Token
from errors import ParserError
from Lexer.lexer import Lexer
from Parser.statements import *
from Parser.expressions import *


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        assert(lexer is not None)
        self.__lexer = lexer
        self.__current_token: Optional[Token] = None
        self.AST = []

        self.__parseProgram()

    def __getNextToken(self) -> Token:
        self.__current_token = self.__lexer.buildToken()
        return self.__current_token

    def __parseProgram(self):
        self.__getNextToken()
        while self.__current_token.type != '#EOF':
            if result := self.__parseClassDefinition():
                self.AST.append(result)
            if result := self.__parseDefinition():
                self.AST.append(result)

    def __parseClassDefinition(self):
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
                while self.__current_token.type != '}':
                    if result := self.__parseDefinition():
                        members.append(result)
                if self.__getNextToken().type != ';':
                    raise ParserError(
                        'Expecting ; after class definition', self.__current_token)
                self.__getNextToken()
            return ClassDefine(
                class_name, base_class, members)

    def __parseDefinition(self):
        if type := self.__parseType():
            if self.__getNextToken().type in ['#ID', 'main']:
                name = self.__current_token.value
            else:
                raise ParserError('Excpecting ID after type',
                                  self.__current_token)
            if self.__getNextToken().type == '(':
                parameters = self.__parseParameters()
                functionBlock = self.__parseStatementBlock()
                return FunctionDefine(type, name, parameters, functionBlock)
            elif self.__current_token.type == ';':
                if name == 'main':
                    raise ParserError(
                        'Variable cannot be named with reserved keyword', self.__current_token)
                if type == 'void':
                    raise ParserError(
                        'Variable cannot be of type void', self.__current_token)
                self.__getNextToken()
                return VariableDefine(type, name)
            else:
                raise ParserError(
                    'Excpecting ; after variable definiton', self.__current_token)

    def __parseParameters(self):
        if self.__current_token.type == '(':
            parameters = []
            while self.__getNextToken().type != ')':
                if len(parameters) > 0 and self.__current_token.type == ',':
                    self.__getNextToken()
                if type := self.__parseType():
                    if self.__getNextToken().type == '#ID':
                        name = self.__current_token.value
                        parameters.append(ParameterDefine(type, name))
                    else:
                        raise ParserError(
                            'Expecting ID after type', self.__current_token)
                elif self.__current_token.type == '{':
                    raise ParserError(
                        'Expecting ) after parameters', self.__current_token)
                else:
                    raise ParserError(
                        'Expecting variable type', self.__current_token)
            self.__getNextToken()
        return parameters

    def __parseArguments(self):
        if self.__current_token.type == '(':
            arguments = []
            while self.__getNextToken().type != ')':
                if len(arguments) > 0 and self.__current_token == ',':
                    self.__getNextToken()
                if result := self.__parseExpression():
                    arguments.append(result)

    def __parseStatementBlock(self):
        if self.__current_token.type == '{':
            operations = []
            self.__getNextToken()
            while self.__current_token.type != '}':
                for try_parse in [self.__parseIfStatement,
                                  self.__parseWhileStatement,
                                  self.__parseReturnStatement,
                                  self.__parseDefinition,
                                  self.__parseAssignStatement,
                                  self.__parseFuncCall]:
                    if operation := try_parse():
                        operations.append(operation)
                        break
            self.__getNextToken()
            return StatementBlock(operations)

    def __parseIfStatement(self):
        if self.__current_token.type == 'if':
            if self.__getNextToken().type == '(':
                self.__getNextToken()
                condition = self.__parseCondition()
                if self.__current_token.type != ')':
                    raise ParserError(
                        "Expecting ) after condition", self.__current_token)
                self.__getNextToken()
                ifBlock = self.__parseStatementBlock()
                elseBlock = None
                if self.__current_token.type == 'else':
                    self.__getNextToken()
                    elseBlock = self.__parseStatementBlock()
                return IfStatement(condition, ifBlock, elseBlock)
            else:
                raise ParserError(
                    "Expecting ( after if token", self.__current_token)

    def __parseWhileStatement(self):
        if self.__current_token.type == 'while':
            if self.__getNextToken().type == '(':
                condition = self.__parseCondition()
                if self.__current_token.type != ')':
                    raise ParserError(
                        'Expecting closing bracket after condition', self.__current_token)
                statementBlock = self.__parseStatementBlock()
                return WhileStatement(condition, statementBlock)
            else:
                raise ParserError(
                    'Expecting ( after while token', self.__current_token)

    def __parseReturnStatement(self):
        if self.__current_token.type == 'return':
            self.__getNextToken()
            return_value = self.__parseExpression()
            if not return_value is None:
                if self.__current_token.type == ';':
                    self.__getNextToken()
                    return ReturnStatement(return_value)
                else:
                    raise ParserError(
                        'Expecting ; after return value', self.__current_token)
            else:
                self.__getNextToken()
                raise ParserError(
                    'Expecting return value after return keyword', self.__current_token)
        pass

    def __parseNestedName(self):
        if self.__current_token.type == '#ID':
            nested_name = [self.__current_token.value]
            while self.__getNextToken().type == '.':
                if self.__getNextToken().type == '#ID':
                    nested_name.append(self.__current_token.value)
                else:
                    raise ParserError('Expecting ID after .',
                                      self.__current_token)
            return nested_name

    def __parseExpression(self):
        lvalue = self.__parseBaseExpression()
        if operator := self.__parseAdditiveOp():
            rvalue = self.__parseExpression()
            return MathExpression(lvalue, operator, rvalue)
        else:
            return Expression(lvalue)

    # TODO: work on base expression and assignment
    def __parseAssignStatement(self, name=None):
        # if name is None:
        #     name = self.__parseNestedName()
        pass

    def __parseBaseExpression(self):
        if negation := self.__current_token.type == '-':
            self.__getNextToken()

        for try_parse in [self.__parseNestedName,
                          self.__parseNumber,
                          self.__parseParenthesesExpression,
                          self.__parseFuncCall, ]:
            if value := try_parse():
                break

        if not negation:
            return BaseExpression(value)
        else:
            return Negation(value)

    def __parseParenthesesExpression(self):
        if self.__current_token.type == '(':
            self.__getNextToken()
            expression = self.__parseExpression()
            if self.__current_token.type == ')':
                self.__getNextToken()
                return ParenthesesExpression(expression)
            else:
                raise ParserError('Expecting ) after expression',
                                  self.__current_token)

    def __parseCondition(self):
        lcond = self.__parseBaseCondition()
        if operator := self.__parseRelationOp():
            rcond = self.__parseBaseCondition()
            return RelationCondition(lcond, operator, rcond)
        return BaseCondition(lcond)

    def __parseBaseCondition(self):
        if self.__parseLogicNegationOp():
            return Negation(self.__parseParenthesesCondition())
        else:
            return self.__parseExpression()

    def __parseParenthesesCondition(self):
        if self.__current_token.type == '(':
            self.__getNextToken()
            condition = self.__parseCondition()
            self.__getNextToken()
            if self.__current_token.type == ')':
                return ParenthesesCondition(condition)
            else:
                raise ParserError('Expecting ) after condition',
                                  self.__current_token)
        else:
            raise ParserError('Expecting ( after !', self.__current_token)

    def __parseType(self):
        if self.__current_token.type in ['int', 'float', 'void', '#ID']:
            return self.__current_token.value
        else:
            return None

    def __parseNumber(self):
        x = self.__current_token
        if x.type in ['#INT_VAL', '#FLOAT_VAL']:
            self.__getNextToken()
            return x.value

    def __parseLogicNegationOp(self):
        x = self.__current_token
        if x.type == '!':
            self.__getNextToken()
            return x.value

    def __parseAssignmentOP(self):
        if self.__current_token.type == '=':
            return self.__current_token.type

    def __parseRelationOp(self):
        x = self.__current_token
        if x.type in ['<', '>', '<=', '=>', '!=', '==']:
            self.__getNextToken()
            return x.value

    def __parseAdditiveOp(self):
        x = self.__current_token
        if x.type in ['-', '+']:
            self.__getNextToken()
            return x.value

    def __parseFuncCall(self, name=None):
        if name is None:
            name = self.__parseNestedName()
        if self.__current_token.type == '(':
            arguments = self.__parseArguments()
            if self.__current_token.type != ')':
                raise ParserError(
                    'Expecting closing bracket after arguments', self.__current_token)
            else:
                return FuncCall(name, arguments)

        elif self.__current_token.type == '=':
            self.__parseAssignStatement(name)
        # else:
        #     return VariableAccess(name)
