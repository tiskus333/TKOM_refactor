from Lexer.lexer import Lexer
from Parser.parser import Parser

if __name__ == "__main__":
    # lexer = Lexer("test tokenizacji stringa -2 2 _23;", direct_input=True)
    # lexer = Lexer("Tests/lexerTest/alltokens.txt")
    # while lexer.buildToken(verbose=True).value != '#EOF':
    #     pass
    if __name__ == '__main__':
        lexer = Lexer(
            'class kot: pies { int fun(int c, float d){if(!(2>4)){a=1;}else{while(x.a.b < -condfun(innerfun())){x.func(c,d);}}} float x; void fun2(){ return 2+3-x;} }; void main(){return 2-3;}', direct_input=True)
        parser = Parser(lexer=lexer)
        print(parser.AST)
