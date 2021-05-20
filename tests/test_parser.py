import unittest
from Lexer.lexer import Lexer
from Parser.parser import Parser
from errors import ParserError
from Parser.types import *


class TestParser(unittest.TestCase):

    def test_ClassDefinition(self):
        lexer = Lexer('class A {};', direct_input=True)
        parser = Parser(lexer)
        classDef = ClassDefine('A', None, [])
        self.assertEqual(parser.AST[0], classDef)

    def test_ClassDefinition_BaseClass(self):
        lexer = Lexer('class A : B {};', direct_input=True)
        parser = Parser(lexer)
        self.assertEqual(parser.AST[0], ClassDefine('A', 'B', []))

    def test_FunctionDefinition_Empty(self):
        lexer = Lexer('int fun(){}', direct_input=True)
        parser = Parser(lexer)
        funDef = FunctionDefine(
            'int', 'fun', [], StatementBlock([]))
        self.assertEqual(parser.AST[0], funDef)

    def test_VariableDefinition(self):
        lexer = Lexer('int x;', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseDefinition()
        varDef = VariableDefine('int', 'x')
        self.assertEqual(result, varDef)

    def test_ParameterDefinition(self):
        lexer = Lexer('(float a,int b, int c)',
                      direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseParameters()
        params = [ParameterDefine('float', 'a'), ParameterDefine(
            'int', 'b'), ParameterDefine('int', 'c')]
        self.assertEqual(result, params)

    def test_ParameterDefinition_empty(self):
        lexer = Lexer('()',
                      direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseParameters()
        self.assertEqual(result, [])

    def test_IfStatement(self):
        lexer = Lexer('if(1>2){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseIfStatement()
        condition = RelationCondition(
            BaseExpression(1), '>', BaseExpression(2))
        ifstatement = IfStatement(condition, StatementBlock([]), None)
        self.assertEqual(result, ifstatement)

    def test_IfElseStatement(self):
        lexer = Lexer('if(1>2){}else{}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseIfStatement()
        condition = RelationCondition(
            BaseExpression(1), '>', BaseExpression(2))
        ifstatement = IfStatement(
            condition, StatementBlock([]), StatementBlock([]))
        self.assertEqual(result, ifstatement)

    def test_WhileStatement(self):
        lexer = Lexer('while(1>2){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseWhileStatement()
        condition = RelationCondition(
            BaseExpression(1), '>', BaseExpression(2))
        whilestatement = WhileStatement(condition, StatementBlock([]))
        self.assertEqual(result, whilestatement)

    def test_ReturnStatement(self):
        lexer = Lexer('return a;', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseReturnStatement()
        returnStatement = ReturnStatement(VariableAccess(['a']))
        self.assertEqual(result, returnStatement)

    def test_StatementBlock(self):
        lexer = Lexer('{ return a;}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseStatementBlock()
        statementBlock = StatementBlock(
            [ReturnStatement(VariableAccess(['a']))])
        self.assertEqual(result, statementBlock)

    def test_StatementBlock_empty(self):
        lexer = Lexer('{}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseStatementBlock()
        statementBlock = StatementBlock([])
        self.assertEqual(result, statementBlock)

    def test_StatementBlock_nested(self):
        lexer = Lexer('{{}}', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseStatementBlock()
        statementBlock = StatementBlock([StatementBlock([])])
        self.assertEqual(result, statementBlock)

    def test_BaseExpression(self):
        lexer = Lexer('1 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseBaseExpression()
        expression = BaseExpression(1)
        self.assertEqual(result, expression)

    def test_MathExpression_simple(self):
        lexer = Lexer('1+2 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseExpression()
        expression = MathExpression(BaseExpression(1), '+', BaseExpression(2))
        self.assertEqual(result, expression)

    def test_MathExpression_advanced(self):
        lexer = Lexer('1+2-x', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseExpression()
        expression = MathExpression(BaseExpression(
            1), '+', MathExpression(BaseExpression(2), '-', VariableAccess(['x'])))
        self.assertEqual(result, expression)

    def test_ParenthesesExpression(self):
        lexer = Lexer('(1+2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseExpression()
        expression = ParenthesesExpression(MathExpression(
            BaseExpression(1), '+', BaseExpression(2)))
        self.assertEqual(result, expression)

    def test_FunctionCall_empty(self):
        lexer = Lexer('func()', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseFuncCall()
        expression = FuncCall(['func'], [])
        self.assertEqual(result, expression)

    def test_FunctionCall_simpleArg(self):
        lexer = Lexer('func(1,x)', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseFuncCall()
        expression = FuncCall(
            ['func'], [BaseExpression(1), VariableAccess(['x'])])
        self.assertEqual(result, expression)

    def test_FunctionCall_nestedArg(self):
        lexer = Lexer('func(fun2(x))', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseFuncCall()
        expression = FuncCall(
            ['func'], [FuncCall(['fun2'], [VariableAccess(['x'])])])
        self.assertEqual(result, expression)

    def test_RelationCondition_simple(self):
        lexer = Lexer('1!=2 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseCondition()
        expression = RelationCondition(
            BaseExpression(1), '!=', BaseExpression(2))
        self.assertEqual(result, expression)

    def test_RelationCondition_advanced(self):
        lexer = Lexer('1!=(x+2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseCondition()
        expression = RelationCondition(
            BaseExpression(1), '!=', ParenthesesExpression(MathExpression(VariableAccess(['x']), '+', BaseExpression(2))))
        self.assertEqual(result, expression)

    def test_ParenthesesCondition(self):
        lexer = Lexer('(1<2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseParenthesesCondition()
        expression = ParenthesesCondition(RelationCondition(
            BaseExpression(1), '<', BaseExpression(2)))
        self.assertEqual(result, expression)

    def test_VariableAccess(self):
        lexer = Lexer('a.b.c', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseVariableAccess()
        expression = VariableAccess(['a', 'b', 'c'])
        self.assertEqual(result, expression)

    def test_Negation_number(self):
        lexer = Lexer('-2 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseExpression()
        expression = Negation(2)
        self.assertEqual(result, expression)

    def test_Negation_variable(self):
        lexer = Lexer('-x', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseExpression()
        expression = Negation(VariableAccess(['x']))
        self.assertEqual(result, expression)

    def test_LogicNegation(self):
        lexer = Lexer('!(1<2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseCondition()
        expression = LogicNegation(ParenthesesCondition(RelationCondition(
            BaseExpression(1), '<', BaseExpression(2))))
        self.assertEqual(result, expression)

    def test_Assignments_number(self):
        lexer = Lexer('x = 2;', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseAssignStatement()
        expression = AssignStatement(['x'], BaseExpression(2))
        self.assertEqual(result, expression)

    def test_Assignments_variable(self):
        lexer = Lexer('x = a;', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseAssignStatement()
        expression = AssignStatement(['x'], VariableAccess(['a']))
        self.assertEqual(result, expression)

    def test_Assignments_function(self):
        lexer = Lexer('x = fun();', direct_input=True)
        parser = Parser(lexer, tests=True)
        result = parser.parseAssignStatement()
        expression = AssignStatement(['x'], FuncCall(['fun'], []))
        self.assertEqual(result, expression)

    def test_Error_Assignment_missing_semicolon(self):
        lexer = Lexer('x = 2 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseAssignStatement()

    def test_Error_Assignment_missing_value(self):
        lexer = Lexer('x = ;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseAssignStatement()

    def test_Error_Name(self):
        lexer = Lexer('a.b.', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseNestedName()

    def test_Error_Return_missing_semicolon(self):
        lexer = Lexer('return x', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseReturnStatement()

    def test_Error_While_missing_left_bracket(self):
        lexer = Lexer('while x<2){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseWhileStatement()

    def test_Error_While_missing_right_bracket(self):
        lexer = Lexer('while(x<2{}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseWhileStatement()

    def test_Error_While_missing_statement(self):
        lexer = Lexer('while(x<2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseWhileStatement()

    def test_Error_IF_missing_left_bracket(self):
        lexer = Lexer('if x<2){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseIfStatement()

    def test_Error_IF_missing_right_bracket(self):
        lexer = Lexer('if(x<2{}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseIfStatement()

    def test_Error_IF_missing_statement(self):
        lexer = Lexer('if(x<2)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseIfStatement()

    def test_Error_emptyExpression(self):
        lexer = Lexer('', direct_input=True)
        parser = Parser(lexer, tests=True)
        self.assertEqual(parser.parseExpression(), None)

    def test_Error_Arguments_missing_argument(self):
        lexer = Lexer('(x,)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseArguments()

    def test_Error_Arguments_missing_bracker_arguments(self):
        lexer = Lexer('(x', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseArguments()

    def test_Error_Parameter_missing_parameter_name(self):
        lexer = Lexer('(int x, int)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseParameters()

    def test_Error_Parameter_missing_parameter(self):
        lexer = Lexer('(int x,)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseParameters()

    def test_Error_Parameter_missing_bracket(self):
        lexer = Lexer('(int x', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseParameters()

    def test_Error_Definiton_missing_semicolon(self):
        lexer = Lexer('int x', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseDefinition()

    def test_Error_Definiton_missing_name(self):
        lexer = Lexer('int ;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseDefinition()

    def test_Error_Definiton_keyword(self):
        lexer = Lexer('int int;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseDefinition()

    def test_Error_Definiton_keyword_2(self):
        lexer = Lexer('int while(){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseDefinition()

    def test_Error_Definiton_void_variable(self):
        lexer = Lexer('void x;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseDefinition()

    def test_Error_Definiton_semicolon_after_func(self):
        lexer = Lexer('void x(){};', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseProgram()

    def test_Error_Class_missing_semicolon(self):
        lexer = Lexer('class x{}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseClassDefinition()

    def test_Error_Class_missing_name(self):
        lexer = Lexer('class {};', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseClassDefinition()

    def test_Error_Class_missing_basename(self):
        lexer = Lexer('class a: {};', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseClassDefinition()

    def test_Error_Class_missing_opening(self):
        lexer = Lexer('class a};', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseClassDefinition()

    def test_Error_Class_missing_closing(self):
        lexer = Lexer('class a{;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseClassDefinition()

    def test_Error_ParenthCond_missing_closing(self):
        lexer = Lexer('(a>b', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseParenthesesCondition()

    def test_Error_ParenthExpr_missing_closing(self):
        lexer = Lexer('(1+2 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseParenthesesExpression()

    def test_Error_Cond_missing_bracket_negation(self):
        lexer = Lexer('!a>b)', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseCondition()

    def test_Error_FuncCall_standalone_semicolon(self):
        lexer = Lexer('{x.func(b)}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseStatementBlock()

    def test_Error_Statement_missing_closing(self):
        lexer = Lexer('{ int x;', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseStatementBlock()

    def test_Error_Program_empty(self):
        lexer = Lexer('1 ', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseProgram()

    def test_Error_Function(self):
        lexer = Lexer('a(){}', direct_input=True)
        parser = Parser(lexer, tests=True)
        with self.assertRaises(ParserError):
            parser.parseProgram()

    def test_print(self):
        lexer = Lexer('Tests/ParserTest1.txt')
        parser = Parser(lexer)
        print(parser.AST)
