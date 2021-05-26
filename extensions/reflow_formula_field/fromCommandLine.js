const context = require("./reflowFormulas")

const base64FormulaString = process.argv[2]
const base64ContextToUse = process.argv[3]
const bufferContext = Buffer.from(base64ContextToUse, 'base64')
const bufferFormula = Buffer.from(base64FormulaString, 'base64')
const formula = bufferFormula.toString('ascii')
const contextToUse = bufferContext.toString('ascii')

const newContext = context(JSON.parse(contextToUse))
const result = JSON.stringify(newContext.eval(formula))

process.stdout.write(result)
