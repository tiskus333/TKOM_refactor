

from Parser.types import *


class StaticAnalyzer(object):
    def __init__(self):
        self.classes = []
        self.functions = []
        self.variables = []

    def traverse(self, AST):
        for node_ in AST:
            if not isinstance(node_, list):
                node_ = [node_]
            for node in node_:
                if isinstance(node, ParserType):
                    if isinstance(node, ClassDefine):
                        self.classes.append(node)
                    elif isinstance(node, FunctionDefine):
                        self.functions.append(node)
                    elif isinstance(node, VariableDefine):
                        self.variables.append(node)

                    self.traverse(node.get_children())
