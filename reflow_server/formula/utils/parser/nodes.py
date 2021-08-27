from reflow_server.formula.utils.settings import NodeType

import json


############################################################################################
class Program:
    node_type = NodeType.PROGRAM

    def __init__(self, block):
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
class Block:
    node_type = NodeType.BLOCK

    def __init__(self, instructions):
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
class IfStatement:
    node_type = NodeType.IF_STATEMENT

    def __init__(self, expression, block, else_statement=None):
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
class ModuleDefinition:
    node_type = NodeType.MODULE_DEFINIITION

    def __init__(self, variable, parameters, module_literals=[]):
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
class ModuleLiteral:
    node_type = NodeType.MODULE_LITERAL

    def __init__(self, variable, block):
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
class Attribute:
    node_type = NodeType.ATTRIBUTE

    def __init__(self, left, right_value, operation):
        self.left = left
        self.right_value = right_value 
        self.operation = operation

    def __str__(self):
        return json.dumps(json.loads(
            (
                '{'
                '   "node": "%s",'
                '   "left": %s, '
                '   "right_value": "%s", '
                '   "operation": %s '
                '}' % (
                    self.node_type,
                    self.left,
                    self.right_value.value,
                    self.operation
                )
            )  
        ), indent=4)
############################################################################################
class FunctionDefinition:
    node_type = NodeType.FUNCTION_DEFINITION

    def __init__(self, variable, parameters, block):
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
class Struct:
    node_type = NodeType.STRUCT

    def __init__(self, name, arguments):
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
class FunctionCall:
    node_type = NodeType.FUNCTION_CALL

    def __init__(self, name, parameters):
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
class BooleanOperation:
    node_type = NodeType.BOOLEAN_OPERATION

    def __init__(self, left, right, operation):
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
class BinaryOperation:
    node_type = NodeType.BINARY_OPERATION

    def __init__(self, left, right, operation):
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
class BinaryConditional:
    node_type = NodeType.BINARY_CONDITIONAL

    def __init__(self, left, right, operation):
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
class UnaryConditional:
    node_type = NodeType.UNARY_CONDITIONAL

    def __init__(self, operation, value):
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
class UnaryOperation:
    node_type = NodeType.UNARY_OPERATION

    def __init__(self, operation, value):
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
class Boolean:
    node_type = NodeType.BOOLEAN

    def __init__(self, value):
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
class Integer:
    node_type = NodeType.INTEGER

    def __init__(self, value):
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
class Float:
    node_type = NodeType.FLOAT

    def __init__(self, value):
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
class String:
    node_type = NodeType.STRING

    def __init__(self, value):
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
class Datetime:
    node_type = NodeType.DATETIME
    
    def __init__(self, value):
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
class Null:
    node_type = NodeType.NULL

    def __init__(self):
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
class Assign:
    node_type = NodeType.ASSIGN

    def __init__(self, left, right, operation):
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
class Variable:
    node_type = NodeType.VARIABLE

    def __init__(self, value):
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
class Slice:
    node_type = NodeType.SLICE

    def __init__(self, left, slice_value):
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
class List:
    node_type = NodeType.LIST

    def __init__(self, members=[]):
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
class Dict:
    node_type = NodeType.DICT

    def __init__(self, members=[]):
        """
        THose members is a 2d array. So the array is like
        [
            [key1, value1],
            [key2, value2]
        ]
        """
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