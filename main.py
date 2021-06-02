from Lexer.lexer import Lexer
from Parser.parser import Parser
from StaticAnalysis.analyzer import StaticAnalyzer


if __name__ == "__main__":

    if __name__ == '__main__':
        lexer = Lexer('Tests/AnalyzerTest1.txt')
        parser = Parser(lexer=lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('GLOBAL', 'A')
        # analyzer.change_class_name('GLOBAL', 'B', 'C')
        # analyzer.change_class_name('GLOBAL', 'C', 'D')
        # analyzer.change_class_name('GLOBAL', 'A', 'F')
        analyzer.save_file(file='my_code.txt')
