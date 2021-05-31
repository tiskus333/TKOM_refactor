

from errors import AnalyzerError
from Parser.types import *


class StaticAnalyzer(object):
    def __init__(self):
        self.classes = {}
        self.functions_def = {}
        self.variables_def = {}
        self.functions = {}
        self.variables = {}
        self.temp_funccall = None
        self.temp_scope = None

    def traverse(self, AST, scope='GLOBAL'):
        for node_ in AST:
            if not isinstance(node_, list):
                node_ = [node_]
            scope_ = scope
            for node in node_:
                if isinstance(node, ParserType):
                    if isinstance(node, ClassDefine):
                        self.check_not_exists_add(scope, node)
                        self.traverse(node.get_children(),
                                      scope_ + '.' + node.class_name)
                    elif isinstance(node, FunctionDefine):
                        self.check_not_exists_add(scope_, node)
                        self.traverse(node.get_children(),
                                      scope_ + '.' + node.name)
                    elif isinstance(node, ParameterDefine):
                        self.check_not_exists_add(scope_, node)
                    elif isinstance(node, VariableDefine):
                        self.check_not_exists_add(scope_, node)
                    elif isinstance(node, FuncCall):
                        self.temp_funccall = node
                        self.temp_scope = scope
                        self.check_exists(scope, node)
                        self.functions[(scope_, node.function_name)] = node
                        self.traverse(node.get_children(),
                                      scope_)
                    elif isinstance(node, VariableAccess):
                        self.check_exists(scope, node)
                        self.variables[(scope_, node.name)] = node
                        self.traverse(node.get_children(),
                                      scope_)
                    else:
                        self.traverse(node.get_children(),
                                      scope_)

    def check_exists(self, scope, node):
        if isinstance(node, VariableAccess):
            if self.check_exists_nested(scope, node.name, variable=True):
                return
            else:
                raise AnalyzerError('Variable', node.name)
        if isinstance(node, FuncCall):
            if self.check_exists_nested(scope, node.function_name, variable=False):
                return
            else:
                raise AnalyzerError('Function', node.function_name)

    def check_not_exists_add(self, scope, node):
        if isinstance(node, ClassDefine):
            if (scope, node.class_name) in self.classes:
                raise AnalyzerError('Class', node.class_name, defined=True)
            self.classes[(scope, node.class_name)] = node
        if isinstance(node, FunctionDefine):
            if (scope, node.name) in self.functions_def:
                raise AnalyzerError('Function', node.name, defined=True)
            self.functions_def[(scope, node.name)] = node
        if isinstance(node, ParameterDefine):
            if (scope, node.name) in self.variables_def:
                raise AnalyzerError('Parameter', node.name, defined=True)
            self.variables_def[(scope, node.name)] = node
        if isinstance(node, VariableDefine):
            if (scope, node.name) in self.variables_def:
                raise AnalyzerError('Variable', node.name, defined=True)
            self.variables_def[(scope, node.name)] = node
        pass

    def check_all_scopes(self, scope, name, list):
        scope = scope.split('.')
        for i in range(0, len(scope)):
            if i == 0:
                scope_ = '.'.join(scope)
            else:
                scope_ = '.'.join(scope[:-i])
            if (scope_, name) in list:
                return list.get((scope_, name))
        return None

    def check_exists_nested(self, scope, name, variable):
        name = name.split('.')
        next_name = name[1:]
        if (var := self.check_all_scopes(scope, name[0], self.variables_def)):
            var_type = var.type
            if var_type in ['int', 'float']:
                return var
            return self.check_contains(var_type, next_name, variable)

        else:
            return None

    def check_contains(self, class_type, name, variable):
        if len(name) == 0:
            return True
        for val in self.classes.keys():
            if class_type in val[1]:
                for member in self.classes[val].members:
                    if isinstance(member, VariableDefine) and variable:
                        if member.name == name[0]:
                            return self.check_contains(member.type, name[1:], variable)
                    if isinstance(member, FunctionDefine) and not variable:
                        return self.match_functions(
                            self.temp_scope, member, self.temp_funccall)

        return False

    def match_functions(self, scope, funcdef, funccall):
        if isinstance(funcdef, FunctionDefine) and isinstance(funccall, FuncCall):
            name = funccall.function_name.split('.')[-1]
            if name == funcdef.name:
                if len(funcdef.parameters) == len(funccall.arguments):
                    for param, arg in zip(funcdef.parameters, funccall.arguments):
                        if isinstance(arg, FuncCall):
                            if (variable := self.check_all_scopes(
                                    scope, arg.function_name, self.functions_def)):
                                if variable.type != param.type:
                                    raise AnalyzerError(
                                        f'Wrong Function return type expected {param.type} got {arg.type}', param.type)
                        if isinstance(arg, VariableAccess):
                            if (variable := self.check_all_scopes(
                                    scope, arg.name, self.variables_def)):
                                if variable.type != param.type:
                                    raise AnalyzerError(
                                        f'Wrong argument type expected {param.type} got {variable.type}', param.type)
                else:
                    raise AnalyzerError(
                        f'Function {name} takes only {len(funcdef.parameters)} parameters, {len(funccall.arguments)} provided', name)
            return True
        return False

    def print_members(self):
        print(self.__dict__)
