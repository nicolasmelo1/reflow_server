from reflow_server.formula.utils import interpreter
from reflow_server.formula.utils.builtins.objects.Error import Error
from reflow_server.formula.utils.lexer import Lexer
from reflow_server.formula.utils.settings import Settings
from reflow_server.formula.utils.context import Context
from reflow_server.formula.utils.parser import Parser
from reflow_server.formula.utils.interpreter import Interpreter

context = Context(flow_context='automation')
settings = Settings(context, is_testing=True)

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

fibonacci(1000)
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
    "teste": "1",
    "teste2": {
        "teste1": 1,
        "teste3": 3,
    }
}
dicionario["teste2"]["teste3"]
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
module Struct(a, b=3, c=5) 
module Teste(a, b)


struct = Struct{a=2, b=5, c=Teste{1, 2}}

struct.c.a = "Ola"

struct.c.a
"""

HTTP_library = r"""
response = HTTP.post(
    url="https://maker.ifttt.com/trigger/registro_atualizado_em_negocios/with/key/UsON56lWobTsQ_9eOXhLXytB6Csg6piJVuJDWfw-Cg",  
    json_data={
        "value1": "nicolasmelo12@gmail.com",
        "value2": ~D[2012-04-12 23:12],
        "value3": "nicolas.melo@reflow.com.br"
    }
)
response.conteudo
"""

SMTP_library = r"""
message = SMTP.build_message("nicolas.melo1@hotmail.com", ["nicolasmelo12@gmail.com"], "Tesssste", "Testinho")
SMTP.send_email("smtp.office365.com", 587, "nicolas.melo1@hotmail.com", "Nicolas1234!@#", message)
"""

List_library = r"""
list = ["a","b","c"]
new_list = List.map(list, function (elem, ind) do
    ind
end)
new_list
"""

automation_library = r"""
Automation.trigger_action({
    "Field 1": "value"
    "Field 2": "value2"
    "field 3": {
        "field": 23
    }
})
"""

from datetime import datetime
from reflow_server.formula.utils.helpers import DatetimeHelper

date_string = f"~D[{datetime.strptime('2012-04-11 11:11:11', '%Y-%m-%d %H:%M:%S').strftime(DatetimeHelper.to_python_format(context.datetime.date_format, context.datetime.time_format))}]"
datetime_test = r"""
# Testar comentários
teste = {
    "": ~D[2020-10-10]
    "Valor": 123
}

teste[""]
"""

functions_to_test = [
    #simple_arithimetic, 
    #function,
    #recursion_and_function_call, 
    #anonymous_formulas,
    #lists,
    #anonymous_function_call,
    dicts,
    #modules,
    #structs,
    #HTTP_library,
    #SMTP_library,
    #datetime_test,
    #List_library,
    #automation_library
]

import json
import time

start = time.time()
for function in functions_to_test:
    value = None
    try:
        lexer = Lexer(function, settings)
        parser = Parser(lexer, settings)
        ast = parser.parse()
        interpreter = Interpreter(settings)
        value = interpreter.evaluate(ast)
    except Error as e:
        value = e
    print(value._representation_())
end = time.time()

print(end-start)
