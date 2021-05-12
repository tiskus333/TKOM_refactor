from Parser.tree import *


class BaseStatement(Node):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children=children)


class ClassDefine(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class FunctionDefine(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class VariableDefine(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class IfStatement(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class WhileStatement(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class ReturnStatement(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class IfStatement(BaseStatement):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)
