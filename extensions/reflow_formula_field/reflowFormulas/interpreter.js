const { settings } = require('./settings')
const memory = require('./memory') 
const helpers = require('./helpers')
const { SyntaxError } = require('./errors')
const builtins = require('./builtins')

/**
 * Used for interpreting the Abstract Syntax Tree generated by the parser.
 * 
 * @param {Object} ast - It's better if you print to understand how it is structured. It is a tree, you can check each node 
 * in parser/nodes.js file.
 * 
 * @returns {Any} - Returns the result of the formula, can be a bool, a string, a integer and so on.
 */
const interpreter = (ast) => {
    const globalMemory = memory()

    /**
     * Main function of the interpreter, if you check the return of the `interpreter` function it is the result of this
     * function.
     * 
     * This works recusively, if you see clearly, whenever we handle a node we call this function is called again. By making this way 
     * this we can interpret the hole Abstract Syntax Tree of the program. Also by returning EVERY handle call, we guarantee that the
     * program t will return something to the user.
     * 
     * @param {Object} node - you can check each node object in parser/nodes.js file.
     * 
     * @returns {Any} - Returns the result of the interpret.
     */
    const interpret = (node, returnFunction=false) => {
        switch (node.nodeType) {
            case settings().NODE_TYPES.FUNCTION_CALL:
                let functionReturn = handleFunctionCall(node)
                if (returnFunction && typeof functionReturn === 'function') {
                    return functionReturn()
                } else {
                    return functionReturn
                }
            case settings().NODE_TYPES.FUNCTION_DEFINITION:
                return handleFunctionDefinition(node)
            case settings().NODE_TYPES.IF_STATEMENT:
                return handleIfStatement(node)
            case settings().NODE_TYPES.PROGRAM:
                return handleProgram(node)
            case settings().NODE_TYPES.VARIABLE:
                return handleVariable(node)
            case settings().NODE_TYPES.ASSIGN:
                return handleAssign(node)
            case settings().NODE_TYPES.BLOCK:
                return handleBlock(node)
            case settings().NODE_TYPES.UNARY_OPERATION:
                return handleUnaryOperation(node)
            case settings().NODE_TYPES.UNARY_CONDITIONAL:
                return handleUnaryConditional(node)
            case settings().NODE_TYPES.BINARY_CONDITIONAL:
                return handleBinaryConditional(node)
            case settings().NODE_TYPES.BINARY_OPERATION:
                return handleBinaryOperation(node)
            case settings().NODE_TYPES.BOOLEAN_OPERATION:
                return handleBooleanOperation(node)
            case settings().NODE_TYPES.NULL:
                return handleNull(node)
            case settings().NODE_TYPES.STRING:
                return handleString(node)
            case settings().NODE_TYPES.FLOAT:
                return handleFloat(node)
            case settings().NODE_TYPES.INTEGER:
                return handleInteger(node)
            case settings().NODE_TYPES.BOOLEAN:
                return handleBoolean(node)
            default:
                return node
        }
    }

    const handleProgram = (node) => {
        const programRecord = globalMemory.record("MAIN",'PROGRAM', 1)
        globalMemory.stack.push(programRecord)
        return interpret(node.block)
    }

    const handleBlock = (node) => {
        const none = new builtins.objects.none()
        let lastValue = none.__initialize__()
        for (let i=0; i<node.instructions.length; i++) {
            lastValue = interpret(node.instructions[i])
        }
        return lastValue
    }

    const handleIfStatement = (node) => {
        const expressionValue = interpret(node.expression)
        if (expressionValue.__boolean__().__representation__()) {
            return interpret(node.block)
        } else if (node.elseStatement) {
            return interpret(node.elseStatement)
        }
    }

    const handleUnaryOperation = (node) => {
        const value = interpret(node.value, true)
        
        switch (node.operation.tokenType) {
            case settings().TOKEN_TYPES.SUM:
                return value.__unaryPlus__()
            case settings().TOKEN_TYPES.SUBTRACTION:
                return value.__unaryMinus__()
        }
    }

    /**
     * Handles inversion in conditionals. Like "not value".
     * 
     * @returns {builtins.objects.boolean} - returns a new boolean instance.
     */
    const handleUnaryConditional = (node) => {
        switch (node.operation.tokenType) {
            case settings().TOKEN_TYPES.INVERSION:
                const value = interpret(node.value, true)
                return value.__boolean__().__not__()
        }
    }

    /**
     * Interprets the Binary Conditionals.
     */
    const handleBinaryConditional = (node) => {
        if ([settings().TOKEN_TYPES.EQUAL, 
            settings().TOKEN_TYPES.DIFFERENT, 
            settings().TOKEN_TYPES.LESS_THAN,
            settings().TOKEN_TYPES.GREATER_THAN,
            settings().TOKEN_TYPES.LESS_THAN_EQUAL,
            settings().TOKEN_TYPES.GREATER_THAN_EQUAL
        ].includes(node.operation.tokenType)) {
            const valueLeft = interpret(node.left, true)
            const valueRight = interpret(node.right, true)

            switch (node.operation.tokenType) {
                case settings().TOKEN_TYPES.EQUAL:
                    return valueLeft.__equals__(valueRight)
                case settings().TOKEN_TYPES.DIFFERENT:
                    return valueLeft.__difference__(valueRight)
                case settings().TOKEN_TYPES.LESS_THAN:
                    return valueLeft.__lessThan__(valueRight)
                case settings().TOKEN_TYPES.GREATER_THAN:
                    return valueLeft.__greaterThan__(valueRight)
                case settings().TOKEN_TYPES.LESS_THAN_EQUAL:
                    return valueLeft.__lessThanEqual__(valueRight)
                case settings().TOKEN_TYPES.GREATER_THAN_EQUAL:
                    return valueLeft.__greaterThanEqual__(valueRight)
            }
        }
    }

    /**
     * Handles when we sum, multiplies, power, division, subtraction of numbers.
     * 
     * MULTIPLICATION:
     * - Multiplying an int with an string repeats the string n times.
     * - We can only multiply strings with integers, otherwise throws an error.
     * - Only multiplication with ints and floats accepted
     * 
     * DIVISION:
     * - Division is only supported by ints or floats
     * 
     * SUBTRACTION:
     * - Subtraction is only supported by ints or floats
     * 
     * SUM:
     * - Sum of two strings concatenates strings
     * - Sum of ints or floats adds them
     * - Sum of other types are not supported
     * 
     * POWER:
     * - Only power of numbers are supported
     */
    const handleBinaryOperation = (node) => {
        let valueLeft = interpret(node.left, true)
        let valueRight = interpret(node.right, true)

        switch (node.operation.tokenType) {
            case settings().TOKEN_TYPES.MULTIPLICATION:
                return valueLeft.__multiply__(valueRight)
            case settings().TOKEN_TYPES.DIVISION:
                return valueLeft.__divide__(valueRight)
            case settings().TOKEN_TYPES.SUBTRACTION:
                return valueLeft.__subtract__(valueRight)
            case settings().TOKEN_TYPES.SUM:
                return valueLeft.__add__(valueRight)
            case settings().TOKEN_TYPES.POWER:
                return valueLeft.__power__(valueRight)
        }
    }

    /**
     * Handle Conjunction or disjunction. Conjunction is "and" operator and disjunction is "or" operator.
     */
    const handleBooleanOperation = (node) => {
        const valueLeft = interpret(node.left, true)
        const valueRight = interpret(node.right, true)

        switch (node.operation.tokenType) {
            case settings().TOKEN_TYPES.CONJUNCTION:
                return valueLeft.__and__(valueRight)
            case settings().TOKEN_TYPES.DISJUNCTION:
                return valueLeft.__or__(valueRight)
        }
    }

    /**
     * When we define a function we add the node
     * @param {*} node 
     * @returns 
     */
    const handleFunctionDefinition = (node) => {
        const functionName = node.variable.value.value
        const func = new builtins.objects.functions()

        const record = globalMemory.stack.peek()

        const functionValue = func.__initialize__(node, record, node.parameters)

        record.assign(functionName, functionValue)
        return functionValue
    }

    const handleFunctionCall = (node) => {
        const functionName = node.name
        const record = globalMemory.stack.peek()
        const functionObject = record.get(functionName)
        
        const createFunctionRecord = () => {
            let functionRecord = globalMemory.record(functionName,'FUNCTION')
            // Define the scope of the function in the new function call stack
            Object.keys(functionObject.scope.members).forEach(key => {
                functionRecord.assign(key, functionObject.scope.members[key])
            })

            // Gets the positional parameters and also the values parameters
            for (let i=0; i<functionObject.parameters.length; i++) {
                let parameterName = null
                let parameterValue = null
                if (node.parameters[i]) {
                    if (functionObject.parameters[i].nodeType === settings().NODE_TYPES.ASSIGN) {
                        parameterName = functionObject.parameters[i].left.value.value 
                    } else {
                        parameterName = functionObject.parameters[i].value.value 
                    }
                    parameterValue = interpret(node.parameters[i])
                } else if (functionObject.parameters[i].nodeType === settings().NODE_TYPES.ASSIGN) {
                    parameterName = functionObject.parameters[i].left.value.value 
                    parameterValue = interpret(functionObject.parameters[i].right)
                } else {
                    throw SyntaxError(`missing parameter of function "${functionName}"`)
                }
                functionRecord.assign(parameterName, parameterValue)
            }

            return functionRecord
        }

        const toEvaluateFunction = (pushToCurrent = false) => {
            const record = createFunctionRecord()

            if (pushToCurrent) globalMemory.stack.pushToCurrent(record)        
            else globalMemory.stack.push(record)        

            const result = interpret(functionObject.astFunction.block)
            
            if (pushToCurrent === false) globalMemory.stack.pop()        
            return result
        }
        // If this condition is set this means we are inside a recursion (we are in a function named fibonacci, and calling it again)
        if (functionName === record.name) {
            return toEvaluateFunction
        } else {
            const functionRecord = createFunctionRecord()
            globalMemory.stack.push(functionRecord)
            let result = interpret(functionObject.astFunction.block)
            while (typeof result === 'function') {
                result = result(true)
            }
            globalMemory.stack.pop()
            return result
        }
    }

    const handleAssign = (node) => {
        const variableName = node.left.value.value
        const variableValue = interpret(node.right)
        const record = globalMemory.stack.peek()
        record.assign(variableName, variableValue)
        const none = new builtins.objects.none()
        return none.__initialize__()
    }

    const handleVariable = (node) => {
        const variableName = node.value.value
        const record = globalMemory.stack.peek()
        return record.get(variableName)
    }

    const handleInteger = (node) => {
        if (helpers.isInteger(node.value)) {
            const int = new builtins.objects.int()
            return int.__initialize__(node.value)
        }
        else {
            throw SyntaxError('Cannot interpret integer')
        }
    }

    const handleBoolean = (node) => {
        if (helpers.isBoolean(node.value)) {
            const boolean = new builtins.objects.boolean()
            return boolean.__initialize__(node.value)
        } else {
            throw SyntaxError('Cannot interpret boolean')
        }
    }

    const handleString = (node) => {
        if (helpers.isString(node.value)) {
            const string = new builtins.objects.string()
            return string.__initialize__(node.value)
        } else {
            throw SyntaxError('Cannot interpret string')
        }
    }

    const handleFloat = (node) => {
        const value = node.value.replace(settings().DECIMAL_POINT_CHARACTER, '.')
        if (helpers.isFloat(value)) {
            const float = new builtins.objects.float()
            return float.__initialize__(value)
        } else {
            throw SyntaxError('Cannot interpret float')
        }
    }

    const handleNull = () => {
        const none = new builtins.objects.none()
        return none.__initialize__()
    }

    return interpret(ast)
}

module.exports = interpreter
