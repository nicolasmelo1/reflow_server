from reflow_server.formula.utils import interpreter
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter

settings = Settings()

simple_arithimetic = r"""(1 + 2) + (2 + 2)"""

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

fibonacci(1000)
"""

anonymous_formulas = r"""
anonymous = function (a, callback) do
    a + callback()
end

anonymous(1, function() do
    2
end)
"""

lists = r"""
array = [1, 2, [3, [4], 1, 2], 5]
array[2][1][0] = "teste"
array
"""


functions_to_test = [
    simple_arithimetic, 
    recursion_and_function_call, 
    anonymous_formulas,
    lists
]

for function in functions_to_test:
    lexer = Lexer(function, settings)
    parser = Parser(lexer, settings)
    ast = parser.parse()
    interpreter = Interpreter(settings)
    value = interpreter.evaluate(ast)
    print(value._representation_())


lexer1 = Lexer(r"""
function fibonacci(n, a=0, b=1) do
    if n == 0 do
        a
    else if n == 1 do
        b
    else do
        fibonacci(n - 1, b, a + b)
    end
end

fibonacci(1000)
""", settings)