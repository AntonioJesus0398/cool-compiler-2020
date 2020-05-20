from collections import deque, namedtuple
from collections.abc import Sequence

# Definition of a Formal
Formal = namedtuple('Formal', ['id', 'type'])

class ASTNode:
    def print_node(self, cur_width = 0, char = '.'):
        cur_padding = cur_width * char

        new_width = cur_width + 5
        new_padding = new_width * char

        if issubclass(self.__class__, Sequence):
            lst = [ ]

            for x in self:
                lst.append(x.print_node(new_width, char))

            joined = ',\n'.join(lst)
            return f"\n{joined}"

        if issubclass(self.__class__, Terminal):
            return f"{self.value}"

        lst = [ f"{cur_padding}{self.__class__.__name__}(" ]

        for attr in self.__dict__:
            name = getattr(self, attr)
            rep = name.print_node(new_width, char)
            lst.append(f"{new_padding}{attr} = {rep}")

        lst.append(f"{cur_padding})")

        return "\n".join(lst)

    def __repr__(self):
        return self.print_node()

class Deque(deque, ASTNode): pass

class Program(ASTNode):
    def __init__(self, class_list = Deque()):
        self.class_list = class_list

class Class(ASTNode):
    def __init__(self, type, opt_inherits, feature_list = Deque()):
        self.type = type
        self.opt_inherits = opt_inherits  #can be None
        self.feature_list = feature_list

class Feature(ASTNode): pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr_list = Deque()):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr_list = expr_list

class Attribute(Feature):
    def __init__(self, formal, opt_init):
        self.formal = formal
        self.opt_init = opt_init  #can be None

class Expr(ASTNode): pass

class Assignment(Expr):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class Dispatch(Expr):
    def __init__(self, expr, opt_type, id, expr_list = Deque()):
        self.expr = expr
        self.opt_type = opt_type  #can be None
        self.id = id
        self.expr_list = expr_list

class SelfDispatch(Expr):
    def __init__(self, id, expr_list = Deque()):
        self.id = id
        self.expr_list = expr_list

class If(Expr):
    def __init__(self, predicate, if_branch, else_branch):
        self.predicate = predicate
        self.if_branch = if_branch
        self.else_branch = else_branch

class While(Expr):
    def __init__(self, predicate, body):
        self.predicate = predicate
        self.body = body

class Block(Expr):
    def __init__(self, expr_list = Deque()):
        self.expr_list = expr_list

class Let(Expr):
    def __init__(self, attribute_list, body):
        self.attribute_list = attribute_list
        self.body = body

class Case(Expr):
    # Case list is a Deque of (Formal, Expr)

    def __init__(self, expr, case_list = Deque()):
        self.expr = expr
        self.case_list = case_list

class New(Expr):
    def __init__(self, type):
        self.type = type

class UnaryOp(Expr):
    def __init__(self, expr):
        self.expr = expr

class IsVoid(UnaryOp): pass
class IntComp(UnaryOp): pass
class Not(UnaryOp): pass

class BinaryOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Plus(BinaryOp): pass
class Minus(BinaryOp): pass
class Mult(BinaryOp): pass
class Div(BinaryOp): pass

class Less(BinaryOp): pass
class LessEq(BinaryOp): pass
class Eq(BinaryOp): pass

class Terminal(ASTNode):
    def __init__(self, value):
        self.value = value

class Int(Expr, Terminal): pass
class String(Expr, Terminal): pass

class Bool(Expr, Terminal): pass
class TrueValue(Bool): pass
class FalseValue(Bool): pass

if __name__ == '__main__':
    plus = Plus(Int(123), Int(65))
    isvoid = IsVoid(Int(5))
    b = Block(Deque([Plus(Int(1), Int(1)), IsVoid(String("asd"))]))

    block = Block(Deque([plus, b, isvoid]))

    print(block)
    print(b)
    print(plus)