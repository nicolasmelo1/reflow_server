from settings import NodeType


class Program:
    node_type = NodeType.PROGRAM

    def __init__(self, block):
        self.block = block


class Block:
    node_type = NodeType.BLOCK

    def __init__(self, instructions):
        self.instructions = instructions


class IfStatement:
    node_type = NodeType.IF_STATEMENT

    def __init__(self, expression, block, else_statement=None):
        self.expression = expression
        self.block = block
        self.else_statament = else_statement


class FunctionDefinition:
    node_type = NodeType.FUNCTION_DEFINITION

    def __init__(self, variable, parameters, block):
        self.variable = variable
        self.parameters = parameters
        self.block = block


class FunctionCall:
    node_type = NodeType.FUNCTION_CALL

    def __init__(self, parameters, name):
        self.parameters = parameters
        self.name = name


class BooleanOperation:
    node_type = NodeType.BOOLEAN_OPERATION

    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation


class BinaryOperation:
    node_type = NodeType.BINARY_OPERATION

    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation


class UnaryConditional:
    node_type = NodeType.UNARY_CONDITIONAL

    def __init__(self, operation, value):
        self.operation = operation
        self.value = value


class UnaryOperation:
    node_type = NodeType.UNARY_OPERATION

    def __init__(self, operation, value):
        self.operation = operation
        self.value = value


class Boolean:
    node_type = NodeType.BOOLEAN

    def __init__(self, value):
        self.value = value


class Integer:
    node_type = NodeType.INTEGER

    def __init__(self, value):
        self.value = value
        

class Float:
    node_type = NodeType.FLOAT

    def __init__(self, value):
        self.value = value


class String:
    node_type = NodeType.STRING

    def __init__(self, value):
        self.value = value


class Null:
    node_type = NodeType.NULL

    def __init__(self):
        self.value = None


class Assign:
    node_type = NodeType.ASSIGN

    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation
        

class Variable:
    node_type = NodeType.VARIABLE

    def __init__(self, value):
        self.value = value
