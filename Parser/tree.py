from typing import List
from Lexer.token import Token


class ASTNode:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()


def printTree(node: ASTNode, depth=0):
    if node != None:
        print(' '*depth, node)
        for n in node.children:
            printTree(n, depth+1)
