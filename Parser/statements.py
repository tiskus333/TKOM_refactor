from Parser.tree import *


class ClassDefine(ASTNode):
    def __init__(self, class_name: str, base_class: str, members: List) -> None:
        self.class_name = class_name
        self.base_class = base_class
        self.members = members

    def __str__(self) -> str:
        return f"\nClass definition: Name={self.class_name}, BaseClass={self.base_class}, \nMembers={self.members}"


class FunctionDefine(ASTNode):
    def __init__(self, return_type, name, parameters, functionBlock) -> None:
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.functionBlock = functionBlock

    def __str__(self) -> str:
        return f"\nFunction definiton: Return type={self.return_type}, Name={self.name}, \nParameters={self.parameters}, \nFunction Block={self.functionBlock}"


class VariableDefine(ASTNode):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        return f"\nVariable definition: Type={self.type}, Name={self.name}"


class ParameterDefine(ASTNode):
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        return f"\nParameter definition: Type={self.type}, Name={self.name}"


class IfStatement(ASTNode):
    def __init__(self, condition, ifBlock, elseBlock=None) -> None:
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

    def __str__(self) -> str:
        return f"\nIF statement: Condition={self.condition}, ifBlock={self.ifBlock}, ElseBlock={self.elseBlock}"


class WhileStatement(ASTNode):
    def __init__(self, condition, statementBlock) -> None:
        self.condition = condition
        self.statementBlock = statementBlock

    def __str__(self) -> str:
        return f"\nWhile statement: Condition={self.condition}, StatementBlock={self.statementBlock}"


class ReturnStatement(ASTNode):
    def __init__(self, returnValue, returnType) -> None:
        self.returnValue = returnValue
        self.returnType = returnType

    def __str__(self) -> str:
        return f"\n"
