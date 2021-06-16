from lexer import Lexer
from settings import Settings
from parser import Parser

settings = Settings()
lexer = Lexer(r"""
variable = 1.00
""", settings)
parser = Parser(lexer, settings)
ast = parser.parse()
print(ast.__dict__)
print(ast.block.__dict__)
print(ast.block.instructions[0].__dict__)