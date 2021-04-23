from Lexer.lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer("Tests/test.txt")
    #lexer = Lexer("test tokenizacji stringa -2 2 _23;", direct_input=True)
    while lexer.buildToken(verbose=True).value != '#EOF':
        pass
