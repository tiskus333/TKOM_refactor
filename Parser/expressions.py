from Parser.tree import *


class BaseExpression(Node):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children=children)


class FuncCall(BaseExpression):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class BaseCondition(Node):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children=children)


class RelationCondition(BaseCondition):
    def __init__(self, value: Token, children: List[Token]) -> None:
        super().__init__(value, children)


class
