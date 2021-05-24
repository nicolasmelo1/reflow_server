const context = require("./reflowFormulas")
const newContext = context()

const base64FormulaString = process.argv[2]
const buffer = Buffer.from(base64FormulaString, 'base64')
const formula = buffer.toString('ascii')

const result = JSON.stringify(newContext.eval(formula))

process.stdout.write(result)
