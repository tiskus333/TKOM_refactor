import unittest
from Lexer.lexer import Lexer
from Parser.parser import Parser
from errors import AnalyzerError, FunctionError
from Parser.types import *
from StaticAnalysis.analyzer import StaticAnalyzer


class TestSemanticErrorrs(unittest.TestCase):

    def test_RepeatClass(self):
        lexer = Lexer('class A {};class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_RepeatVariable(self):
        lexer = Lexer('class A {int x; int x;};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_RepeatParameter(self):
        lexer = Lexer('class A {void fun(int i, int i){}};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UnknownClassType(self):
        lexer = Lexer('class A {}; B b;', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UnknownClassInheritance(self):
        lexer = Lexer('class A:B {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UnknownClassInheritance2(self):
        lexer = Lexer('class A:B {}; class B{};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UndeclaredVariable(self):
        lexer = Lexer('void main(){x=2;}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UndeclaredMemberVariable(self):
        lexer = Lexer('class A {}; A a; void main(){a.x=2;}',
                      direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UndeclaredFunction(self):
        lexer = Lexer('void main(){fun();}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_UndeclaredMemberFunction(self):
        lexer = Lexer('class A {}; A a; void main(){a.f();}',
                      direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(AnalyzerError):
            analyzer.traverse(parser.AST)

    def test_WrongFunctionArgumentLength(self):
        lexer = Lexer(
            'class A {void f(int i, int j){}}; A a; void main(){a.f(1,2,3);}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)

    def test_WrongArgumentType(self):
        lexer = Lexer(
            'class A {void f(int i, int j){}}; A a; void main(){float x; a.f(x,2);}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)

    def test_VoidReturnNonVoid(self):
        lexer = Lexer(
            'class A {int f(int i, int j){return;}}; A a; void main(){a.f(1,2);}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)

    def test_NonVoidReturnVoid(self):
        lexer = Lexer(
            'class A {void f(int i, int j){return 2;}}; A a; void main(){a.f(1,2);}', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)


class TestRename(unittest.TestCase):
    def test_ClassRename_1(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('GLOBAL', 'A', 'B')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/1.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_2(self):
        lexer = Lexer('class A {};\nA a;', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('GLOBAL', 'A', 'B')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/2.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_3(self):
        lexer = Lexer('class A {A a;};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('GLOBAL', 'A', 'B')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/3.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_4(self):
        lexer = Lexer('class A {A a;};\nclass C:A{};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('GLOBAL', 'A', 'B')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/4.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_5(self):
        lexer = Lexer(
            'class A {A fun(A a1, A a2){return a1;}};\nclass C:A{};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('GLOBAL', 'A', 'B')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/5.txt').read()
        self.assertEqual(out, expected)
