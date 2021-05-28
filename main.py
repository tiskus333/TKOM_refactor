from Lexer.lexer import Lexer
from Parser.parser import Parser
from StaticAnalysis.analyzer import StaticAnalyzer


if __name__ == "__main__":

    if __name__ == '__main__':
        lexer = Lexer('Tests/ParserTest1.txt')
        parser = Parser(lexer=lexer)
        analyzer = StaticAnalyzer()
        analyzer.traverse(parser.AST)
        print("classes:", analyzer.classes)
        print("functions:", analyzer.functions)
        print("variables:", analyzer.variables)
        # print(parser.AST)
        # for node in parser.AST:
        #     print("node: ", node.get_children())
