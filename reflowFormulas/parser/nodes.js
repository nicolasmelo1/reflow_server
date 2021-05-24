const { settings } = require('../settings')


/**
 * Handles Unary Operations, Unary operations are stuff like: -1 or +1. As you can see
 * -1 and +1 ARE NOT binary, they doesn't have a left operand, just the right value of the operation sign.
 * 
 * @param {Token} operation - The Token object
 * @param {String} value - The value of this unary expression
 * @returns {Object} - {
 *      nodeType: {Enum} - settings().NODE_TYPES.UNARY_OPERATION
 *      operation: {Token} - The Token object,
 *      value: {String} - The value of this unary expression
 * }
 */
const UnaryOperation = (operation, value) => {
    return {
        nodeType: settings().NODE_TYPES.UNARY_OPERATION,
        operation: operation,
        value: value
    }
}

/**
 * Handles Unary Conditionals, similar to Unary Operation, unary conditionals are unary value but that evaluate conditional. 
 * Like "not". The expression "not False" should be "true" and "not True", should be "false". We transform the result from this
 * unary in boolean values.
 *   
 * @param {Token} operation - The Token object
 * @param {String} value - The value of this unary expression
 * @returns {Object} - {
 *      nodeType: {Enum} - settings().NODE_TYPES.UNARY_CONDITIONAL
 *      operation: {Token} - The Token object,
 *      value: {String} - The value of this unary expression
 * }
 */
const UnaryConditional = (operation, value) => {
    return {
        nodeType: settings().NODE_TYPES.UNARY_CONDITIONAL,
        operation: operation,
        value: value
    }
}

const BooleanOperation = (left, right, operation) => {
    return {
        nodeType: settings().NODE_TYPES.BOOLEAN_OPERATION,
        left,
        right,
        operation
    }
}

const BinaryOperation = (left, right, operation) => {
    return {
        nodeType: settings().NODE_TYPES.BINARY_OPERATION,
        left,
        right,
        operation
    }
}

const BinaryConditional = (left, right, operation) => {
    return {
        nodeType: settings().NODE_TYPES.BINARY_CONDITIONAL,
        left,
        right,
        operation
    }
}

const Boolean = (token) => {
    return {
        nodeType: settings().NODE_TYPES.BOOLEAN,
        value: token.value === settings().BOOLEAN_KEYWORDS[0] ? true : false
    }
}

const Integer = (token) => {
    return {
        nodeType: settings().NODE_TYPES.INTEGER,
        value: token.value
    }
}

const Float = (token) => {
    const value = token.value.replace(settings().DECIMAL_POINT_CHARACTER, '.')
    return {
        nodeType: settings().NODE_TYPES.FLOAT,
        value: value
    }
}

const String = (token) => {
    return {
        nodeType: settings().NODE_TYPES.STRING,
        value: token.value
    }
}

const Null = () => {
    return {
        nodeType: settings().NODE_TYPES.NULL,
        value: null
    }
}

const Assign = (left, right, operation) => {
    return {
        nodeType: settings().NODE_TYPES.ASSIGN,
        left: left,
        right: right,
        operation: operation
    }
}

const Variable = (value) => {
    return {
        nodeType: settings().NODE_TYPES.VARIABLE,
        value: value 
    }
}

const IfStatement = (expression, block, elseStatement=null) => {
    return {
        nodeType: settings().NODE_TYPES.IF_STATEMENT,
        expression: expression,
        block: block,
        elseStatement: elseStatement
    }
}

const FunctionCall = (name, parameters) => {
    return {
        nodeType: settings().NODE_TYPES.FUNCTION_CALL,
        parameters: parameters,
        name: name
    }
}

const FunctionDefinition = (variable, parameters, block) => {
    return {
        nodeType: settings().NODE_TYPES.FUNCTION_DEFINITION,
        variable: variable,
        parameters: parameters,
        block: block
    }
}

const Block = (instructions) => {
    return {
        nodeType: settings().NODE_TYPES.BLOCK,
        instructions: instructions
    }
}

const Program = (block) => {
    return {
        nodeType: settings().NODE_TYPES.PROGRAM,
        block: block
    }
}

module.exports = {
    IfStatement,
    UnaryOperation,
    UnaryConditional,
    BinaryConditional,
    BooleanOperation,
    BinaryOperation,
    Boolean,
    String,
    Float,
    Integer,
    Null,
    Assign,
    Variable,
    Block,
    Program,
    FunctionCall,
    FunctionDefinition
}