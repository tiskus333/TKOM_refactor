import unittest
from Lexer.lexer import Lexer
from errors import LexerError


class TestLexer(unittest.TestCase):
    def test_CheckKeywords(self):
        lexer = Lexer("Tests/lexerTest/alltokens.txt")
        ExpectedTokenList = ["main", "class", "if", "else", "void", "float", "int", "return",  "while",
                             '(', ')', '{', '}', ':', ';', '.', '!', '=', '+', '-', '<', '>', '==', '!=', '<=', '>=', 0, 1, 10, 12, 1234567890, 2, float(0.12), float(1.234), float(5.6667), float(0.001), "_test1", "test_2", "$test3", "_test_4_"]
        for i in range(len(ExpectedTokenList)):
            self.assertEqual(lexer.buildToken().value, ExpectedTokenList[i])

    def test_UnknownToken(self):
        lexer = Lexer("^ * % / ? [ ] @ ~ ` \" \ | & ", direct_input=True)
        with self.assertRaises(LexerError):
            lexer.buildToken()

    def test_InvalidNumber(self):
        lexer = Lexer("12.a", direct_input=True)
        with self.assertRaises(LexerError):
            lexer.buildToken()

    def test_NotFinishedNumber(self):
        lexer = Lexer("12.", direct_input=True)
        with self.assertRaises(LexerError):
            lexer.buildToken()

    def test_SplitNumberID(self):
        lexer = Lexer("12t_2", direct_input=True)
        expectedTokens = [12, "t_2"]
        for i in range(len(expectedTokens)):
            self.assertEqual(lexer.buildToken().value, expectedTokens[i])

    def test_TabInsteadSpace(self):
        lexer = Lexer("cos\ta", direct_input=True)
        expectedTokens = ["cos", "a"]
        for i in range(len(expectedTokens)):
            self.assertEqual(lexer.buildToken().value, expectedTokens[i])

    def test_Comment(self):
        lexer = Lexer("token#test komentarza", direct_input=True)
        expectedTokens = ["token"]
        for i in range(len(expectedTokens)):
            self.assertEqual(lexer.buildToken().value, expectedTokens[i])


if __name__ == '__main__':
    unittest.main()
