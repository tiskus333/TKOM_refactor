from Parser.tree import *


class BaseExpression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"\nBasicExpression: Value={self.value};"


class Expression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"\nExpression: Value={self.value};"


class MathExpression(ASTNode):
    def __init__(self, lvalue, operator, rvalue) -> None:

        self.lvalue = lvalue
        self.rvalue = rvalue
        self.operator = operator

    def __str__(self) -> str:
        return f"\nMathExpression: Operator={self.operator}, Lvalue={self.lvalue}, Rvalue={self.rvalue};"


class ParenthesesExpression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"\nParenthesesExpression: Value={self.value};"


class FuncCall(ASTNode):
    def __init__(self, function_name, arguments) -> None:

        self.function_name = function_name
        self.arguments = arguments

    def __str__(self) -> str:
        return f'\nFunctionCall: FunctionName = {self.function_name}, Arguments = {self.arguments};'


class BaseCondition(ASTNode):
    def __init__(self, condition) -> None:
        self.condition = condition

    def __str__(self) -> str:
        return f"\nBasicCondition: Condition={self.condition};"


class RelationCondition(ASTNode):
    def __init__(self, lcond, operator, rcond) -> None:
        self.lcond = lcond
        self.operator = operator
        self.rcond = rcond

    def __str__(self) -> str:
        return f"\nRelationCondition: Operator={self.operator}, Lcond={self.lcond}, Rcond={self.rcond};"


class ParenthesesCondition(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"\nParenthesesCondition: Value={self.value};"


class VariableAccess(ASTNode):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"\nVariableAccess {self.name};"


class Negation(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"\nNegation: Value={self.value};"
