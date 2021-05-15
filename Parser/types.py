from typing import List


tree_print_offset = 0


class ASTNode(object):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.__str__()


class ClassDefine(ASTNode):
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


class FunctionDefine(ASTNode):
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


class VariableDefine(ASTNode):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Variable definition: Type={self.type}; Name={self.name}"
        tree_print_offset -= 4
        return ret


class ParameterDefine(ASTNode):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Parameter definition: Type={self.type}; Name={self.name}"
        tree_print_offset -= 4
        return ret


class IfStatement(ASTNode):
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


class WhileStatement(ASTNode):
    def __init__(self, condition, statementBlock) -> None:
        self.condition = condition
        self.statementBlock = statementBlock

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}While statement: {self.condition}; {self.statementBlock}"
        tree_print_offset -= 4
        return ret


class ReturnStatement(ASTNode):
    def __init__(self, returnValue) -> None:
        self.returnValue = returnValue

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ReturnStatement: {self.returnValue}"
        tree_print_offset -= 4
        return ret


class StatementBlock(ASTNode):
    def __init__(self, statements) -> None:
        self.statements = statements

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 2
        ret = f"\n{' '*tree_print_offset}StatementBlock:{self.statements}"
        tree_print_offset -= 2
        return ret


class AssignStatement(ASTNode):
    def __init__(self, assignee, expression) -> None:
        self.assignee = assignee
        self.expression = expression

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}AssignStatement: Assignee={self.assignee}; {self.expression}"
        tree_print_offset -= 4
        return ret


class BaseExpression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}BasicExpression: {self.value}"
        tree_print_offset -= 4
        return ret


class Expression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Expression: {self.value}"
        tree_print_offset -= 4
        return ret


class MathExpression(ASTNode):
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


class ParenthesesExpression(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ParenthesesExpression: {self.value}"
        tree_print_offset -= 4
        return ret


class FuncCall(ASTNode):
    def __init__(self, function_name, arguments) -> None:

        self.function_name = function_name
        self.arguments = arguments

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}FunctionCall: FunctionName={self.function_name}, Arguments={self.arguments}"
        tree_print_offset -= 4
        return ret


class BaseCondition(ASTNode):
    def __init__(self, condition) -> None:
        self.condition = condition

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}BasicCondition: {self.condition}"
        tree_print_offset -= 4
        return ret


class RelationCondition(ASTNode):
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


class ParenthesesCondition(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}ParenthesesCondition: {self.value}"
        tree_print_offset -= 4
        return ret


class VariableAccess(ASTNode):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}VariableAccess: Name={self.name}"
        tree_print_offset -= 4
        return ret


class Negation(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}Negation: {self.value}"
        tree_print_offset -= 4
        return ret


class LogicNegation(ASTNode):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        global tree_print_offset
        tree_print_offset += 4
        ret = f"\n{' '*tree_print_offset}LogicNegation: {self.value}"
        tree_print_offset -= 4
        return ret
