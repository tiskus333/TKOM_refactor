from typing import List
import pickle

tree_print_offset = 0


class ParserType(object):

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and pickle.dumps(self) == pickle.dumps(other)

    def get_children(self):
        return self.__dict__.values()


class ClassDefine(ParserType):
    def __init__(self, class_name: str, base_class: str, members: List) -> None:
        self.class_name = class_name
        self.base_class = base_class
        self.members = members

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\nClass definition: Name={self.class_name}; BaseClass={self.base_class}; \n{' '*tree_print_offset}Members={self.members};"
        tree_print_offset -= 4
        return ret


class FunctionDefine(ParserType):
    def __init__(self, return_type, name, parameters, functionBlock) -> None:
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.functionBlock = functionBlock

    def __str__(self) -> str:
        global tree_print_offset
        ret = f"\n{' '*tree_print_offset}Function definiton: ReturnType = {self.return_type}; Name = {self.name}; "
        tree_print_offset += 4
        ret += f"\n{' '*tree_print_offset}Parameters={self.parameters};{self.functionBlock}"
        tree_print_offset -= 4
        return ret


class VariableDefine(ParserType):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Variable definition: Type={self.type}; Name={self.name}"
        tree_print_offset -= 4
        return ret


class ParameterDefine(ParserType):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Parameter definition: Type={self.type}; Name={self.name}"
        tree_print_offset -= 4
        return ret


class IfStatement(ParserType):
    def __init__(self, condition, ifBlock, elseBlock=None) -> None:
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}IfStatement:{self.condition}; {self.ifBlock}; {self.elseBlock}"
        tree_print_offset -= 4
        return ret


class WhileStatement(ParserType):
    def __init__(self, condition, statementBlock) -> None:
        self.condition = condition
        self.statementBlock = statementBlock

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}While statement: {self.condition}; {self.statementBlock}"
        tree_print_offset -= 4
        return ret


class ReturnStatement(ParserType):
    def __init__(self, returnValue) -> None:
        self.returnValue = returnValue

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ReturnStatement: {self.returnValue}"
        tree_print_offset -= 4
        return ret


class StatementBlock(ParserType):
    def __init__(self, statements) -> None:
        self.statements = statements

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 2
        ret = f"\n{' '*tree_print_offset}StatementBlock:{self.statements}"
        tree_print_offset -= 2
        return ret


class AssignStatement(ParserType):
    def __init__(self, assignee, expression) -> None:
        self.assignee = assignee
        self.expression = expression

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}AssignStatement: Assignee={self.assignee}; {self.expression}"
        tree_print_offset -= 4
        return ret


class BaseExpression(ParserType):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}BasicExpression: {self.value}"
        tree_print_offset -= 4
        return ret


class MathExpression(ParserType):
    def __init__(self, lvalue, operator, rvalue) -> None:

        self.lvalue = lvalue
        self.rvalue = rvalue
        self.operator = operator

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}MathExpression: operator {self.operator}, {self.lvalue}, {self.rvalue}"
        tree_print_offset -= 4
        return ret


class ParenthesesExpression(ParserType):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ParenthesesExpression: {self.value}"
        tree_print_offset -= 4
        return ret


class FuncCall(ParserType):
    def __init__(self, function_name, arguments) -> None:

        self.function_name = function_name
        self.arguments = arguments

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}FunctionCall: FunctionName={self.function_name}, Arguments={self.arguments}"
        tree_print_offset -= 4
        return ret


class RelationCondition(ParserType):
    def __init__(self, lcond, operator, rcond) -> None:
        self.lcond = lcond
        self.operator = operator
        self.rcond = rcond

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}RelationCondition: operator {self.operator},{self.lcond}, {self.rcond}"
        tree_print_offset -= 4
        return ret


class ParenthesesCondition(ParserType):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ParenthesesCondition: {self.value}"
        tree_print_offset -= 4
        return ret


class VariableAccess(ParserType):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}VariableAccess: Name={self.name}"
        tree_print_offset -= 4
        return ret


class Negation(ParserType):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Negation: {self.value}"
        tree_print_offset -= 4
        return ret


class LogicNegation(ParserType):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}LogicNegation: {self.value}"
        tree_print_offset -= 4
        return ret
