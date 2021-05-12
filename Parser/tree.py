from typing import List
from Lexer.token import Token


class Node:
    def __init__(self, value: Token, children: List[Token] = []) -> None:
        self.value: Token = value
        self.children: List[Token] = children

    def __str__(self):
        return str(self.value)


def printTree(node: Node, depth=0):
    if node != None:
        print(' '*depth, node)
        for n in node.children:
            printTree(n, depth+1)
