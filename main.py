from Lexer.lexer import Lexer
from Parser.parser import Parser
from Parser.tree import printTree

if __name__ == "__main__":
    #lexer = Lexer("test tokenizacji stringa -2 2 _23;", direct_input=True)
    # lexer = Lexer("Tests/lexerTest/alltokens.txt")
    # while lexer.buildToken(verbose=True).value != '#EOF':
    #     pass
    if __name__ == '__main__':
        lexer = Lexer(
            'class kot: pies { int fun(int c, float d){} float x; void fun2(){} }', direct_input=True)
        parser = Parser(lexer=lexer)
        print(parser.AST[0])
