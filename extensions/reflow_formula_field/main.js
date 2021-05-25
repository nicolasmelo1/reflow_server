const context = require("./reflowFormulas");
const newContext = context()

/*
const newContext = context()
const fomula1 = `
x = 2
if x > 1 and x == 3 do
    "é maior que 1"
else do
    "é menor que 1"
end
`
console.log(fomula1)
console.log(newContext.eval(fomula1))
console.log(`-----------------------`)

const fomula2 = `
not None
`
console.log(fomula2)
console.log(newContext.eval(fomula2))
console.log(`-----------------------`)

const fomula3 = `
x = 2
x
`
console.log(fomula3)
console.log(newContext.eval(fomula3))
console.log(`-----------------------`)

const fomula4 = `
function hello() do
    "olá mundo"
end

function greetings(hello_function) do
    hello_function()
end

greetings(hello)
`
console.log(fomula4)
console.log(newContext.eval(fomula4))
console.log(`-----------------------`)


const fomula5 = `
function hello() do
    x = 2
    function greetings() do
        x + 1
    end
end

teste = hello()

teste()
`
console.log(fomula5)
console.log(newContext.eval(fomula5))
console.log(`-----------------------`)
*/
const fomula5 = `
function hello() do
    x = 2
    function greetings() do
        x + 1
    end
end

teste = hello()

teste()
`
asdasdasd
console.log(JSON.stringify(newContext.eval(fomula5)))
//console.log(evaluator('1 + 2 - 3 and 3 + 5 + 0'))
//console.log(evaluator('"a" * 3'))
//console.log(evaluator('2 < Sum(2;3) and - 6 < 3'))