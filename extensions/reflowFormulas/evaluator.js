const lexer = require('./lexer')
const parser = require('./parser')
const interpreter = require('./interpreter')

const evaluator = (expression) => {
    const syntaxAnalyzer = lexer(expression)
    const ast = parser(syntaxAnalyzer)
    return interpreter(ast)
    
}

module.exports = evaluator