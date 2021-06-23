from reflow_server.formula.utils import interpreter
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter

settings = Settings()
lexer = Lexer(r"""
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
parser = Parser(lexer, settings)
ast = parser.parse()
interpreter = Interpreter(settings)
value = interpreter.evaluate(ast)
print(value._representation_())