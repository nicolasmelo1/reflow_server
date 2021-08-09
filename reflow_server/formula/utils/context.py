############################################################################################
class BuiltinLibraryStruct:
    def __init__(self, struct_name):
        self.struct_name = struct_name
        self.attributes = {}
    # ------------------------------------------------------------------------------------------
    def add_attribute(self, attribute_name, translated_attribute_name):
        self.attributes[attribute_name] = translated_attribute_name
############################################################################################
class BuiltinLibraryMethod:
    def __init__(self, method_name):
        self.method_name = method_name
        self.parameters = {}
    # ------------------------------------------------------------------------------------------
    def add_parameter(self, parameter_name, translated_parameter_name):
        self.parameters[parameter_name] = translated_parameter_name
############################################################################################
class BuiltinLibraryModule:
    """
    This is supposed to have the following structure, so it's easy to index and search for the translation
    in the tree.

    This is built like this.
    To build like this we use helper methods so it's easier to build this structure
    
    >>> {
        "HTTP": BuiltinLibraryModule(
            module_translation='Requisição',
            struct_parameters={
                "name": "nome"
            },
            methods={
                "get": BuiltinLibraryMethod(
                    method_name='pegar',
                    attributes={
                        "url": "endereço",
                        "method": "metodo"
                    }
                ),
                "post": BuiltinLibraryMethod(
                    method_name='subir',
                    attributes={
                        "url": "endereço",
                        "method": "metodo"
                    }
                )
            },
            structs={
                "HTTPResponse": BuiltinLibraryStruct(
                    struct_name='Resposta'
                    attributes={
                        "status_code": "codigo_de_status"
                    }
                )
            }
        )
    }
    """
    def __init__(self, module_name):
        self.module_name = module_name
        self.stuct_parameters = {}
        self.methods = {}
        self.structs = {}
    # ------------------------------------------------------------------------------------------``
    def add_method(self, original_method_name, method_name_translation):
        new_library_method = BuiltinLibraryMethod(method_name_translation)
        self.methods[original_method_name] = new_library_method
        return new_library_method
    # ------------------------------------------------------------------------------------------
    def add_struct(self, original_struct_name, struct_name_translation):
        new_library_struct = BuiltinLibraryStruct(struct_name_translation)
        self.structs[original_struct_name] = new_library_struct
        return new_library_struct
    # ------------------------------------------------------------------------------------------
    def add_struct_parameter(self, original_struct_parameter, struct_parameter_translation):
        self.stuct_parameters[original_struct_parameter] = struct_parameter_translation
############################################################################################
class If:
    def __init__(self, if_keyword, else_keyword):
        self.if_keyword = if_keyword
        self.else_keyword = else_keyword
############################################################################################
class Boolean:
    def __init__(self, true, false):
        self.true = true
        self.false = false
############################################################################################
class Block:
    def __init__(self, do, end):
        self.do = do
        self.end = end
############################################################################################
class Keywords:
    def __init__(self, includes, inversion, disjunction, conjunction, function, module, null, block, boolean, if_block):
        self.includes = includes
        self.inversion = inversion
        self.disjunction = disjunction
        self.conjunction = conjunction
        self.module = module
        self.function = function
        self.null = null
        self.block = block
        self.boolean = boolean
        self.if_block = if_block
############################################################################################
class Context:
    def __init__(self, includes='in', conjunction='and', disjunction='or', inversion='not', 
                 block_do='do', block_end='end', null='None', boolean_true='True',
                 boolean_false='False', if_if='if', if_else='else', function='function',
                 module='module', decimal_point_separator='.', positional_argument_separator=','):
        """
        Responsible for creating the context for the formula evaluation, with this we can translate the formulas to other
        languages, which is something impossible in languages like python, javascript or others.

        Args:
            includes (str, optional): The includes, in python it is known as "in", "in" in python is a generator for iterators, in our case
                                      it's just for boolean. Defaults to 'in'.
            conjunction (str, optional): The conjunction, also known as "&&" in other languages or "and" in python. Defaults to 'and'.
            disjunction (str, optional): The disjunction, also known as "||" in other languages or "or" in python. Defaults to 'or'.
            inversion (str, optional): The inversion, also known as '!' in other languages or "not" in python. Defaults to 'not'.
            block_do (str, optional): The start of the block, on some languages you might remember the '{' and in ruby or elixir 'do'. 
                                      Defaults to 'do'.
            block_end (str, optional): The end of the block, on some languages you might remember the '}' and in ruby or elixir 'end'. 
                                       Defaults to 'end'.
            null (str, optional): The null kewyword, also known as "null" in other languages or "None" in python. Defaults to 'None'.
            boolean_true (str, optional): The boolean True keyword. In python it is "True", on other languages can be "true". 
                                          Defaults to 'True'.
            boolean_false (str, optional): The boolean False keyword. In python it is "False", on other languages can be "false". 
                                           Defaults to 'False'.
            if_if (str, optional): The if keyword to start a logic gate, mostly known as "if". Defaults to 'if'.
            if_else (str, optional): The else keyword when the conditional logic gate is not satisfied, mostly known as "else". 
                                     Defaults to 'else'.
            function (str, optional): The function keyword to create a new function. On python it is like "def". Defaults to 'function'.
            module (str, optional): The module keyword to create a new module. This is similar to a python class, EXCEPT, all methods 
                                    and attributes are static.
            decimal_point_separator (str, optional): The decimal point separator, usually on most languages it is represented as '.', 
                                                     but we can translate to ',' if needed. Defaults to '.'.
            positional_argument_separator (str, optional): The positional arguments separator, on most languages it is represented
                                                           as ',', but on others like excel this can be ';'. Defaults to ','.
        """
        block = Block(block_do, block_end)
        boolean = Boolean(boolean_true, boolean_false)
        if_block = If(if_if, if_else)

        self.keyword = Keywords(
            includes, 
            inversion, 
            disjunction, 
            conjunction, 
            function, 
            module,
            null, 
            block, 
            boolean, 
            if_block
        )
        self.positional_argument_separator = positional_argument_separator
        self.decimal_point_separator = decimal_point_separator
        self.library = {}
    # ------------------------------------------------------------------------------------------
    def add_library_module(self, original_module_name, module_name_translation):
        new_library = BuiltinLibraryModule(module_name_translation)
        self.library[original_module_name] = new_library
        return new_library