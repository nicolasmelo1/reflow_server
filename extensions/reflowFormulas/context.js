const { setContext } = require('./settings')
const evaluator = require('./evaluator')


const context = (contextOptions) => {
    setContext(contextOptions)
    const eval = (expression) => {
        return evaluator(expression)
    }
    return {
        eval
    }
}

module.exports = context