

from os import name
from errors import AnalyzerError
from Parser.types import *


class StaticAnalyzer(object):
    def __init__(self):
        self.clear()

    def clear(self):
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
                        self.check_base_class(scope, node)
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
            if self.check_exists_nested(scope, node.name):
                return
            else:
                raise AnalyzerError('Variable', node.name)
        if isinstance(node, FuncCall):
            if self.check_exists_nested(scope, node.function_name):
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

    def check_exists_nested(self, scope, name):
        name = name.split('.')
        next_name = name[1:]
        if (var := self.check_all_scopes(scope, name[0], self.variables_def)):
            var_type = var.type
            if var_type in ['int', 'float']:
                return var
            return self.check_contains(var, next_name)

        else:
            return None

    def check_contains(self, var, name):
        if len(name) == 0:
            return var
        for val in self.classes.keys():
            if var.type in val[1]:
                check_classes = self.concat_class_members(self.classes[val])
                for member in check_classes:
                    if member.name == name[0]:
                        if isinstance(member, VariableDefine):
                            return self.check_contains(member, name[1:])
                        if isinstance(member, FunctionDefine):
                            return self.match_functions(self.temp_scope, member, self.temp_funccall)
        return None

    def match_functions(self, scope, funcdef, funccall):
        if isinstance(funcdef, FunctionDefine) and isinstance(funccall, FuncCall):
            name = funccall.function_name.split('.')[-1]
            if name == funcdef.name:
                if len(funcdef.parameters) == len(funccall.arguments):
                    for param, arg in zip(funcdef.parameters, funccall.arguments):
                        if isinstance(arg, FuncCall):
                            self.temp_funccall = arg
                            if (variable := self.check_exists_nested(
                                    scope, arg.function_name)):
                                if variable.return_type != param.type:
                                    raise AnalyzerError(
                                        f'Wrong Function return type expected {param.type} got {arg.type}', param.type)
                        if isinstance(arg, VariableAccess):
                            if (variable := self.check_exists_nested(
                                    scope, arg.name)):
                                if variable.type != param.type:
                                    raise AnalyzerError(
                                        f'Wrong argument type expected {param.type} got {variable.type}', param.type)
                else:
                    raise AnalyzerError(
                        f'Function {name} takes only {len(funcdef.parameters)} parameters, {len(funccall.arguments)} provided', name)
            return funcdef
        return None

    def check_base_class(self, scope, node):
        if node.base_class:
            name = node.base_class if isinstance(
                node.base_class, str) else node.base_class.class_name
            if (base_class := self.check_all_scopes(scope, name, self.classes)):
                node.base_class = base_class
            else:
                raise AnalyzerError(
                    'Base Class', node.base_class, defined=False)

    def concat_class_members(self, classDef: ClassDefine):
        members = []
        while classDef.base_class:
            members += classDef.members
            classDef = classDef.base_class
        members += classDef.members
        return members

    def print_members(self):
        print(self.__dict__)

    def save_file(self, tree, file):
        with open(file, 'w') as f:
            for node in tree:
                f.write(node.to_text())

    def change_class_name(self, scope, old_name, new_name):
        change_class = self.classes.get((scope, old_name))

        for var_def in self.variables_def.values():
            if var_def.type == change_class.class_name:
                var_def.type = new_name
        for func_def in self.functions_def.values():
            if func_def.return_type == change_class.class_name:
                func_def.return_type = new_name

        change_class.class_name = new_name
        self.clear()
