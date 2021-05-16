from Lexer.lexer import Lexer
from Parser.parser import Parser


if __name__ == "__main__":

    if __name__ == '__main__':
        lexer = Lexer('Tests/ParserTest1.txt')
        parser = Parser(lexer=lexer)
        print(parser.AST)
