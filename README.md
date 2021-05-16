# TKOM_2021
Projekt na przedmiot TKOM 21L. Refaktoryzacja kodu.

# Pobranie wymaganych pakietow
pip3 install coverage
# Uruchomienie programu
python main.py
# Uruchomienie testow
coverage run -m  unittest discover -v; coverage xml; coverage report -m

# Przykładowe wypisanie drzewa
[
Class definition: Name=kot; BaseClass=pies; 
    Members=[
    Function definiton: ReturnType = int; Name = fun; 
        Parameters=[
            Parameter definition: Type=int; Name=c,   
            Parameter definition: Type=float; Name=d];
          StatementBlock:[
              IfStatement:
                  LogicNegation:
                      ParenthesesCondition:
                          RelationCondition: operator >,
                              BasicExpression: 2,
                              BasicExpression: 4;
                StatementBlock:[
                    AssignStatement: Assignee=['a'];
                        BasicExpression: 1];
                StatementBlock:[
                    While statement:
                        RelationCondition: operator <,
                            VariableAccess: Name=['x', 'a', 'b'],
                            Negation:
                                FunctionCall: FunctionName=['condfun'], Arguments=[
                                    FunctionCall: FunctionName=['innerfun'], Arguments=[]];
                      StatementBlock:[
                          FunctionCall: FunctionName=['x', 'func'], Arguments=[
                              VariableAccess: Name=['c'],
                              VariableAccess: Name=['d']],
                          AssignStatement: Assignee=['a'];
                              ParenthesesExpression:
                                  MathExpression: operator -,
                                      BasicExpression: 2,
                                      VariableAccess: Name=['x']]]],
        Variable definition: Type=float; Name=x,
    Function definiton: ReturnType = void; Name = fun2;
        Parameters=[];
          StatementBlock:[
              ReturnStatement:
                  MathExpression: operator +,
                      BasicExpression: 2,
                      MathExpression: operator -,
                          BasicExpression: 3,
                          VariableAccess: Name=['x']]];,
Function definiton: ReturnType = void; Name = main;
    Parameters=[];
      StatementBlock:[
          ReturnStatement:
              MathExpression: operator -,
                  BasicExpression: 2,
                  BasicExpression: 3]]