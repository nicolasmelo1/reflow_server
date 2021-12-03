from reflow_server.formula.utils.settings import NodeType

import json
import uuid

############################################################################################
class Node:
    def __init__(self):
        self.node_id = str(uuid.uuid4())
############################################################################################
class Program(Node):
    node_type = NodeType.PROGRAM

    def __init__(self, block):
        super(Program, self).__init__()
        self.block = block
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "block": %s '
                '}' % (self.node_type, self.block)
            )
        ), indent=4)
############################################################################################
class Block(Node):
    node_type = NodeType.BLOCK

    def __init__(self, instructions):
        super(Block, self).__init__()
        self.instructions = instructions
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "instructions": [%s] '
                '}' % (
                    self.node_type,
                    ','.join([f'{instruction}' for instruction in self.instructions])
                )
            )
        ), indent=4)
############################################################################################
class IfStatement(Node):
    node_type = NodeType.IF_STATEMENT

    def __init__(self, expression, block, else_statement=None):
        super(IfStatement, self).__init__()
        self.expression = expression
        self.block = block
        self.else_statement = else_statement
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "expression": %s, '
                '   "block": %s, '
                '   "else_statement": %s '
                '}' % (
                    self.node_type,
                    self.expression,
                    self.block,
                    self.else_statement
                )
            )
        ), indent=4)
############################################################################################
class ModuleDefinition(Node):
    node_type = NodeType.MODULE_DEFINIITION

    def __init__(self, variable, parameters, module_literals=[]):
        super(ModuleDefinition, self).__init__()
        self.variable = variable
        self.parameters = parameters
        self.module_literals = module_literals

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "variable": %s, '
                '   "parameters": [%s], '
                '   "module_literals": [%s] '
                '}' % (
                    self.node_type,
                    self.variable,
                    ','.join([f'{parameter}' for parameter in self.parameters]) if self.parameters else '',
                    ','.join([f'{module_literal}' for module_literal in self.module_literals])
                )
            )  
        ), indent=4)
############################################################################################
class ModuleLiteral(Node):
    node_type = NodeType.MODULE_LITERAL

    def __init__(self, variable, block):
        super(ModuleLiteral, self).__init__()
        self.variable = variable
        self.block = block
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "variable": %s, '
                '   "block": %s '
                '}' % (
                    self.node_type,
                    self.variable,
                    self.block
                )
            )  
        ), indent=4)
############################################################################################
class Attribute(Node):
    node_type = NodeType.ATTRIBUTE

    def __init__(self, left, right_value):
        super(Attribute, self).__init__()
        self.left = left
        self.right_value = right_value 

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right_value": "%s" '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right_value.value
                )
            )  
        ), indent=4)
############################################################################################
class FunctionDefinition(Node):
    node_type = NodeType.FUNCTION_DEFINITION

    def __init__(self, variable, parameters, block):
        super(FunctionDefinition, self).__init__()
        self.variable = variable
        self.parameters = parameters
        self.block = block
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "variable": %s, '
                '   "parameters": [%s], '
                '   "block": %s '
                '}' % (
                    self.node_type,
                    self.variable if self.variable else '""',
                    ','.join([f'{parameter}' for parameter in self.parameters]) if self.parameters else '',
                    self.block
                )
            )  
        ), indent=4)
############################################################################################
class Struct(Node):
    node_type = NodeType.STRUCT

    def __init__(self, name, arguments):
        super(Struct, self).__init__()
        self.arguments = arguments
        self.name = name
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "name": %s, '
                '   "arguments": [%s] '
                '}' % (
                    self.node_type,
                    self.name,
                    ','.join([f'{argument}' for argument in self.arguments]) if self.arguments else 'null',
                )
            )  
        ), indent=4)
############################################################################################
class FunctionCall(Node):
    node_type = NodeType.FUNCTION_CALL

    def __init__(self, name, parameters):
        super(FunctionCall, self).__init__()
        self.parameters = parameters
        self.name = name
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "name": %s, '
                '   "parameters": [%s] '
                '}' % (
                    self.node_type,
                    self.name,
                    ','.join([f'{parameter}' for parameter in self.parameters]) if self.parameters else '',
                )
            )  
        ), indent=4)
############################################################################################
class BooleanOperation(Node):
    node_type = NodeType.BOOLEAN_OPERATION

    def __init__(self, left, right, operation):
        super(BooleanOperation, self).__init__()
        self.left = left
        self.right = right
        self.operation = operation
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right": %s, '
                '   "operation": "%s" '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right,
                    self.operation.value,
                )
            )  
        ), indent=4)
############################################################################################
class BinaryOperation(Node):
    node_type = NodeType.BINARY_OPERATION

    def __init__(self, left, right, operation):
        super(BinaryOperation, self).__init__()
        self.left = left
        self.right = right
        self.operation = operation
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right": %s, '
                '   "operation": "%s" '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right,
                    self.operation.value,
                )
            )  
        ), indent=4)
############################################################################################
class BinaryConditional(Node):
    node_type = NodeType.BINARY_CONDITIONAL

    def __init__(self, left, right, operation):
        super(BinaryConditional, self).__init__()
        self.left = left
        self.right = right
        self.operation = operation
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right": %s, '
                '   "operation": "%s" '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right,
                    self.operation.value
                )
            )
        ), indent=4)  
############################################################################################
class UnaryConditional(Node):
    node_type = NodeType.UNARY_CONDITIONAL

    def __init__(self, operation, value):
        super(UnaryConditional, self).__init__()
        self.operation = operation
        self.value = value
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "operation": "%s", ',
                '   "value": %s '
                '}' % (
                    self.node_type,
                    self.operation.value,
                    self.value
                )
            )
        ), indent=4)   
############################################################################################
class UnaryOperation(Node):
    node_type = NodeType.UNARY_OPERATION

    def __init__(self, operation, value):
        super(UnaryOperation, self).__init__()
        self.operation = operation
        self.value = value
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "operation": "%s", ',
                '   "value": %s '
                '}' % (
                    self.node_type,
                    self.operation.value,
                    self.value
                )
            )  
        ), indent=4) 
############################################################################################
class Boolean(Node):
    node_type = NodeType.BOOLEAN

    def __init__(self, value):
        super(Boolean, self).__init__()
        self.value = value

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            )
        ), indent=4) 
############################################################################################
class Integer(Node):
    node_type = NodeType.INTEGER

    def __init__(self, value):
        super(Integer, self).__init__()
        self.value = value

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            )  
        ), indent=4) 
############################################################################################
class Float(Node):
    node_type = NodeType.FLOAT

    def __init__(self, value):
        super(Float, self).__init__()
        self.value = value
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            )  
        ), indent=4) 
############################################################################################
class String(Node):
    node_type = NodeType.STRING

    def __init__(self, value):
        super(String, self).__init__()
        self.value = value

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            ) 
        ), indent=4) 
############################################################################################
class Datetime(Node):
    node_type = NodeType.DATETIME
    
    def __init__(self, value):
        super(Datetime, self).__init__()
        self.value = value
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            ) 
        ))
############################################################################################
class Null(Node):
    node_type = NodeType.NULL

    def __init__(self):
        super(Null, self).__init__()
        self.value = None
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value
                )
            ) 
        ), indent=4) 
############################################################################################
class Assign(Node):
    node_type = NodeType.ASSIGN

    def __init__(self, left, right, operation):
        super(Assign, self).__init__()
        self.left = left
        self.right = right
        self.operation = operation
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right": %s, '
                '   "operation": "%s" '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right,
                    self.operation.value
                )
            )
        ), indent=4) 
############################################################################################
class Variable(Node):
    node_type = NodeType.VARIABLE

    def __init__(self, value):
        super(Variable, self).__init__()
        self.value = value

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "value": "%s" '
                '}' % (
                    self.node_type,
                    self.value.value
                )
            )
        ), indent=4) 
############################################################################################
class Slice(Node):
    node_type = NodeType.SLICE

    def __init__(self, left, slice_value):
        super(Slice, self).__init__()
        self.left = left
        self.slice = slice_value

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "slice": %s '
                '}' % (
                    self.node_type,
                    self.left,
                    self.slice
                )
            )
        ), indent=4) 
############################################################################################
class List(Node):
    node_type = NodeType.LIST

    def __init__(self, members=[]):
        super(List, self).__init__()
        self.members = members

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "members": [%s] '
                '}' % (
                    self.node_type,
                    ','.join([f"{member}" for member in self.members]) if self.members else self.members,
                )
            )
        ), indent=4) 
############################################################################################
class Dict(Node):
    node_type = NodeType.DICT

    def __init__(self, members=[]):
        """
        THose members is a 2d array. So the array is like
        [
            [key1, value1],
            [key2, value2]
        ]
        """
        super(Dict, self).__init__()
        self.members = members
    
    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "members": [%s] '
                '}' % (
                    self.node_type,
                    ','.join([('{'
                    '   "key": %s,'
                    '   "value": %s '
                    '}' % (member[0], member[1])) for member in self.members]) if self.members else self.members,
                )
            )
        ), indent=4) 
############################################################################################