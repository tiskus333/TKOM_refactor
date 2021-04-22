import unittest
from Lexer.lexer import Lexer
from errors import LexerError

ExpectedTokenList = ["main", "class", "if", "else", "void", "float", "int", "return",  "while",
                     "(", ")", "{", "}", ";", ".", "!", "=", "+", "-", "<", ">", 0, 1, 10, 12, 1234567890, 2, float(0.12), float(1.234), float(5.6667), float(0.001), "_test1", "test_2", "$test3", "_test_4_"]


class TestLexer(unittest.TestCase):
    token_list = []

    @classmethod
    def setUP(cls):
        cls.lexer = Lexer("alltokens.txt")
        for _ in range(len(ExpectedTokenList)):
            cls.token_list.append(cls.lexer.buildToken())

    def test_CheckKeywords(self):
        for t, et in zip(self.token_list, ExpectedTokenList):
            self.assertEqual(t, et)

    def test_UnknownToken(self):
        lexer3 = Lexer("^ * % / ? [ ] @ ~ ` \" \ | & ", direct_input=True)
        with self.assertRaises(LexerError):
            for i in range(20):
                lexer3.buildToken()


if __name__ == '__main__':
    unittest.main()
