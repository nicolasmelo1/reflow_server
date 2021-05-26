const evaluator = require('./evaluator')


/*console.log(evaluator(`
function outer() do
    function main() do
        "é isso ai"
    end
end

x = outer()
x()
`))*/

module.exports = require('./context')