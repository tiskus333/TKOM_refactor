from lexer.lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer(path_name="tests/test.txt")
    for i in range(200):
        lexer.buildToken()
