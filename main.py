from Lexer.lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer("totot\n12.b", direct_input=True)
    #lexer = Lexer("Tests/lexerTest/errorfile.txt")
    #lexer = Lexer("test tokenizacji stringa -2 2 _23;", direct_input=True)
    while lexer.buildToken(verbose=True).value != '#EOF':
        pass
