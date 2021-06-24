# Python implementation of Reflow formulas
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter
from reflow_server.formula.utils.context import Context


def evaluate(expression, context=None):
    if context == None:
        context = Context()
    settings = Settings()
    lexer = Lexer(expression, settings)
    parser = Parser(lexer, settings)
    ast = parser.parse()

    interpreter = Interpreter(settings)
    value = interpreter.evaluate(ast)
    return value