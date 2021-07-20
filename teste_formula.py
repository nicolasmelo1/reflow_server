from reflow_server.formula.utils import interpreter
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter

settings = Settings()

simple_arithimetic = r"""(1 + 2) + (2 + 2)"""

function = r"""
function soma(b=1, a) do
    b + a
end

soma(a=2)
"""

recursion_and_function_call = r"""
function fibonacci(n, a=0, b=1) do
    if n == 0 do
        a
    else if n == 1 do
        b
    else do
        fibonacci(n - 1, b, a + b)
    end
end

fibonacci(5)
"""

anonymous_formulas = r"""
anonymous = function(a, callback) do
    a + callback()
end

anonymous(10, function() do
    4
end)
"""

lists = r"""
array = [1, 2, [3, [4], 1, 2], 5]
array[2][1][0] = "teste"
array
"""

anonymous_function_call = r"""
(function (b) do
    function(a) do
        a + b
    end
end)(2)(3)
"""

dicts = r"""
dicionario = {
    "teste": [1, 2, {
        "teste com lista": function() do
            3
        end
    }]
}
dicionario["teste"][2]["teste com lista"]()
"""

modules = r"""
module Modulo do
    function teste() do
        3
    end
end

module Modulo1 do
    function metodo1() do
        Modulo
    end
end


Modulo1.metodo1().teste()
"""

structs = r"""
module Struct(a, b=3, c=5) do 
    function soma(a, b) do
        a + b
    end
end


struct = Struct{a=2, b=5, 10}

Struct.soma(struct.a, struct.c)
"""

functions_to_test = [
    #simple_arithimetic, 
    #function,
    #recursion_and_function_call, 
    #anonymous_formulas,
    #lists,
    #anonymous_function_call,
    #dicts,
    #modules,
    structs
]

for function in functions_to_test:
    lexer = Lexer(function, settings)
    parser = Parser(lexer, settings)
    ast = parser.parse()
    interpreter = Interpreter(settings)
    value = interpreter.evaluate(ast)
    print(value._representation_())

"""
import traceback

class Teste:
    def teste(self):
        print(traceback.print_stack())

teste = Teste()
teste.teste()
"""