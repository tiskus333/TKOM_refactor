# TKOM_2021
Projekt na przedmiot TKOM 21L. Refaktoryzacja kodu.

# Pobranie wymaganych pakietow
pip3 install coverage
# Uruchomienie programu
python3 main.py -i in.txt -o out.txt -r DoZmiany PoZmianie
python3 main.py -i in.txt -o out.txt -m KlasaPochodna

Więcej opcji:

python3 main.py -h
# Uruchomienie testow
```
coverage run -m  unittest discover -v; coverage xml; coverage report -m
```
# Przykładowe działanie programu 
```
python3 main.py -m NowaNazwa -r C NowaNazwa -i my_code.txt -o out.txt
```
### **Przed**
```C++
class Z
{
};
class B : Z
{
	int c;
	int funB;
	void funB()
	{
		if(c > 2)
		{
			c = 2;
		}
		 else
		{
			B zmienna;
			c = c + 1;
		}
	}
};
class C : B
{
};
class A : Z
{
	int c;
	int funB;
	void funB()
	{
		if(c > 2)
		{
			c = 2;
		}
		 else
		{
			B zmienna;
			c = c + 1;
		}
	}
	int a;
	B b;
	int fun(int x, int y)
	{
		y = y + a;
		return x + y;
	}
	B fun2(B b1, B b2)
	{
		return b1.funB + b2.funB;
	}
};
A ob;
void main()
{
	ob.a = 2;
	float y;
	ob.fun(1, ob.fun(1, 2));
	ob.b.c = 1;
	ob.b.funB = 2;
	ob.funB();
}
```
### **Po**
```C++
class Z
{
};
class NowaNazwa : Z
{
	int c;
	int funB;
	void funB()
	{
		if(c > 2)
		{
			c = 2;
		}
		 else
		{
			NowaNazwa zmienna;
			c = c + 1;
		}
	}
};
class A : Z
{
	int c;
	int funB;
	void funB()
	{
		if(c > 2)
		{
			c = 2;
		}
		 else
		{
			NowaNazwa zmienna;
			c = c + 1;
		}
	}
	int a;
	NowaNazwa b;
	int fun(int x, int y)
	{
		y = y + a;
		return x + y;
	}
	NowaNazwa fun2(NowaNazwa b1, NowaNazwa b2)
	{
		return b1.funB + b2.funB;
	}
};
A ob;
void main()
{
	ob.a = 2;
	float y;
	ob.fun(1, ob.fun(1, 2));
	ob.b.c = 1;
	ob.b.funB = 2;
	ob.funB();
}

```
# Przykładowe wypisanie drzewa
```[
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
                            VariableAccess: Name=['x.a.b'],
                            Negation:
                                FunctionCall: FunctionName=['condfun'], Arguments=[
                                    FunctionCall: FunctionName=['innerfun'], Arguments=[]];
                      StatementBlock:[
                          FunctionCall: FunctionName=['x.func'], Arguments=[
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
```