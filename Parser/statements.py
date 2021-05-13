from Parser.tree import *


class ClassDefine(ASTNode):
    def __init__(self, class_name: str, base_class: str, variables: List, functions: List) -> None:
        self.class_name = class_name
        self.base_class = base_class
        self.variables = variables
        self.functions = functions

    def __str__(self) -> str:
        return f"\nClass definition: Name={self.class_name}, Base class={self.base_class}, \nMember variables={self.variables}, \nMember functions={self.functions}"


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
    def __init__(self, condition, IfBlock, elseBlock=None) -> None:
        self.condition = condition
        self.IfBlock = IfBlock
        self.elseBlock = elseBlock

    def __str__(self) -> str:
        return f"\nIF statement: Condition={self.condition}, IfBlock={self.IfBlock}, ElseBlock={self.elseBlock}"


class WhileStatement(ASTNode):
    def __init__(self) -> None:
        self.condition

    def __str__(self) -> str:
        return f"\n"


class ReturnStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f"\n"


class IfStatement(ASTNode):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f""
