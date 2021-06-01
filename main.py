from Lexer.lexer import Lexer
from Parser.parser import Parser
from StaticAnalysis.analyzer import StaticAnalyzer


if __name__ == "__main__":

    if __name__ == '__main__':
        lexer = Lexer('Tests/AnalyzerTest1.txt')
        parser = Parser(lexer=lexer)
        analyzer = StaticAnalyzer()
        analyzer.traverse(parser.AST)
        analyzer.change_class_name('GLOBAL', 'B', 'C')
        analyzer.traverse(parser.AST)
        analyzer.change_class_name('GLOBAL', 'C', 'D')
        analyzer.save_file(parser.AST, file='my_code.txt')
