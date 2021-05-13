from Parser.tree import *


class BaseExpression(ASTNode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f""


class MathExpression(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.lvalue
        self.rvalue
        self.operator

    def __str__(self) -> str:
        return f""


class FuncCall(BaseExpression):
    def __init__(self) -> None:
        super().__init__()
        self.function_name = []
        self.arguments = []

    def __str__(self) -> str:
        return f""


class BaseCondition(ASTNode):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f""


class RelationCondition(BaseCondition):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f""


class ParenthesesCondition(BaseCondition):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f""
