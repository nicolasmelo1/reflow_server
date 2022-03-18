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

fibonacci(30)
"""

recursion = r"""
function fibonacci(n) do
    if n <= 1 do
        n
    else do
        fibonacci(n - 1) + fibonacci(n - 2)
    end
end

fibonacci(30)
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


struct = Struct{a=2, b=[1, 2, function (a, b) do a + b end], c=Teste{1, function (a, b) do a + b end}}

struct.b[2](1, 2)
"""

HTTP_library = r"""
resposta_login = HTTP.post("https://api.auvo.com.br/v2/login/", json_data={
    "apiKey": "ewBfzwn2UjDH8wAdWQSIMgPzmYH9N6",
    "apiToken": "ewBfzwn2UjLvgWIk8Tq0kejfE6uS"
})
if resposta_login.status_code == 200 do
    access_token = resposta_login.json["result"]["accessToken"]
    resposta_criacao_de_task = HTTP.post("https://api.auvo.com.br/v2/tasks/",
        headers={
            "Authorization": "Bearer " + access_token
        }, 
        json_data={
            "taskType": 83344,
            "idUserFrom": 99075,
            "idUserTo": 99075,
            "taskDate": "2022-03-18T18:00:00",
            "latitude": -23.5533909,
            "longitude": -46.6542179,
            "address": "Rua Frei Caneca, 485, 96B",
            "orientation": "Gotta Catch 'Em All",
            "priority": 3
        }
    )

    if resposta_criacao_de_task.status_code == 201 do
      "Criado com sucesso"
    else do
       resposta_criacao_de_task.json
    end
else do
    "Algo de errado não está certo"
end
"""

SMTP_library = r"""
message = SMTP.build_message("ir@irinstalacoes.com.br", ["nicolas.melo@reflow.com.br"], "Teste", "Fulano, a sua apólice acabou de ser emitida e está vigente")

SMTP.send_email("mail.irinstalacoes.com.br", 587, "ir@irinstalacoes.com.br", "ir.instal@123", message)
"""

List_library = r"""
list = ["a","b","c"]
variable = "teste"
new_list = List.for_each(list, function (elem, ind) do
    variable = variable + elem
end)
variable
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

#date_string = f"~D[{datetime.strptime('2012-04-11 11:11:11', '%Y-%m-%d %H:%M:%S').strftime(DatetimeHelper.to_python_format(context.datetime.date_format, context.datetime.time_format))}]"
datetime_test = r"""
date1 =  ~D[2020-10-10]
date2 = ~D[2021-11-11]

Datetime.date_add(date2, months = 20.4)
"""

float_test = r"""1.2 * 1.5"""

functions_to_test = [
    #simple_arithimetic, 
    #function,
    #recursion,
    #recursion_and_function_call, 
    #anonymous_formulas,
    #lists,
    #anonymous_function_call,
    #dicts,
    #modules,
    #structs,
    HTTP_library,
    #SMTP_library,
    #datetime_test,
    #List_library,
    #automation_library,
    #datetime_test,
    #float_test
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

#print(end-start)
