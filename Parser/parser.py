from errors import ParserError
from Lexer.lexer import Lexer


class Parser:
    def __init__(self, source) -> None:
        self.lexer = Lexer(source)
        self.source = source
        self.obj_position = 0
        pass

    def parseProgram(self):
        objects = []

        return objects

    def parseClassDefinition(self):
        pass

    def parseFunctionDefinition(self):
        pass

    def parseParameters(def):
        pass

    def parseArguments(self):
        pass

    def parseStatementBlock(self):
        pass

    def parseIfStatement(self):
        pass

    def parseWhileStatement(self):
        pass

    def parseReturnStatement(self):
        pass

    def parseDefineStatement(self):
        pass

    def parseAssignStatement(self):
        pass

    def parseExpression(self):
        pass

    def parseBaseExpression(self):
        pass

    def parseParenthesesExpr(self):
        pass

    def parseCondition(self):
        pass

    def parseRelationCondition(self):
        pass

    def parseBaseCondition(self):
        pass

    def parseParenthesesCondition(self):
        pass

    def parseArithmeticNegationOp(self):
        pass

    def parseLogicNegationOp(self):
        pass

    def parseAssignmentOP(self):
        pass

    def parseEqualOp(self):
        pass

    def parseRelationOp(self):
        pass

    def parseAdditiveOp(self):
        pass

    def parseFuncCall(self):
        pass
