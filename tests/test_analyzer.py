import unittest
from Lexer.lexer import Lexer
from Parser.parser import Parser
from errors import AnalyzerError, ExecutionError, FunctionError
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

    def test_WrongArgumentType_function(self):
        lexer = Lexer(
            'class A {void f(int i, int j){}}; A a; float f_zla(){return 3;}void main(){float x; a.f(f_zla(),2);}', direct_input=True)
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

    def test_WrongReturn_variable(self):
        lexer = Lexer(
            'class A {float f(int i, int j){return i;}};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)

    def test_WrongReturn_function(self):
        lexer = Lexer(
            'class A {int x(){}float f(int i, int j){return x();}};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(FunctionError):
            analyzer.traverse(parser.AST)


class TestRename(unittest.TestCase):

    def test_ClassMerge_noClass(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(ExecutionError):
            analyzer.change_class_name('C', 'B', 'GLOBAL')

    def test_ClassMerge_nameExists(self):
        lexer = Lexer('class A {};class B {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(ExecutionError):
            analyzer.change_class_name('A', 'B', 'GLOBAL')

    def test_ClassMerge_ReservedName(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(ExecutionError):
            analyzer.change_class_name('A', 'main', 'GLOBAL')

    def test_ClassRename_1(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('A', 'B', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/1.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_2(self):
        lexer = Lexer('class A {};\nA a;', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('A', 'B', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/2.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_3(self):
        lexer = Lexer('class A {A a;};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('A', 'B', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/3.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_4(self):
        lexer = Lexer('class A {A a;};\nclass C:A{};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('A', 'B', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/4.txt').read()
        self.assertEqual(out, expected)

    def test_ClassRename_5(self):
        lexer = Lexer(
            'class A {A fun(A a1, A a2){return a1;}};\nclass C:A{};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('A', 'B', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/rename_examples/5.txt').read()
        self.assertEqual(out, expected)


class test_Merge(unittest.TestCase):
    def test_ClassMerge_noBaseClass(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(ExecutionError):
            analyzer.merge_classes('A', 'GLOBAL')

    def test_ClassMerge_noClass(self):
        lexer = Lexer('class B {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        with self.assertRaises(ExecutionError):
            analyzer.merge_classes('A', 'GLOBAL')

    def test_ClassMerge_1(self):
        lexer = Lexer('class B{}; class A : B {};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('A', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/merge_examples/1.txt').read()
        self.assertEqual(out, expected)

    def test_ClassMerge_2(self):
        lexer = Lexer(
            'class B{int b;}; class A : B {int a;};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('A', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/merge_examples/2.txt').read()
        self.assertEqual(out, expected)

    def test_ClassMerge_3(self):
        lexer = Lexer(
            'class B{int b;}; class A : B {int a;}; class C:B{int c;};', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('A', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/merge_examples/3.txt').read()
        self.assertEqual(out, expected)

    def test_ClassMerge_4(self):
        lexer = Lexer(
            'class B{int b;}; class A : B {int a;}; B b;', direct_input=True)
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('A', 'GLOBAL')
        out = analyzer.to_code()
        expected = open('Tests/merge_examples/4.txt').read()
        self.assertEqual(out, expected)


class test_NormalUsages(unittest.TestCase):
    def test_usage1(self):
        lexer = Lexer('Tests/normal_examples/in/example1.txt')
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.change_class_name('DoZmiany', 'PoZmianie', 'GLOBAL')
        analyzer.save_file('Tests/normal_examples/out/example1.txt')

    def test_usage2(self):
        lexer = Lexer('Tests/normal_examples/in/example2.txt')
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('Pochodna', 'GLOBAL')
        analyzer.save_file('Tests/normal_examples/out/example2.txt')

    def test_usage3(self):
        lexer = Lexer('Tests/normal_examples/in/example3.txt')
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('B', 'GLOBAL')
        analyzer.save_file('Tests/normal_examples/out/example3.txt')

    def test_usage4(self):
        lexer = Lexer('Tests/normal_examples/in/example4.txt')
        parser = Parser(lexer)
        analyzer = StaticAnalyzer(parser)
        analyzer.merge_classes('B', 'GLOBAL')
        analyzer.save_file('Tests/normal_examples/out/example4.txt')
