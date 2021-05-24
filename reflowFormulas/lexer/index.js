const { settings } = require('../settings')
const TOKEN = require('./token')
const errors = require('../errors') 

const reserved = (expression, nextPosition, position) => {
    let cachedReservedCharacters = []

    const getReservedToken = () => {
        let reserved = expression[position.current]
        nextPosition()
        if (reserved !== settings().POSITIONAL_ARGUMENT_SEPARATOR) {
            while (![
                ' ', 
                null, 
                undefined, 
                settings().POSITIONAL_ARGUMENT_SEPARATOR,
                '\n',
                '=',
                '(', 
                ')',
                ...settings().BINARY_OPERATIONS_TO_TOKENS.keys()
            ].includes(expression[position.current])) {
                reserved = reserved + expression[position.current]
                nextPosition()
            }
        }
        if (settings().BOOLEAN_KEYWORDS.includes(reserved)) {
            return TOKEN(reserved, settings().TOKEN_TYPES.BOOLEAN)
        } else if (settings().NULL_KEYWORD === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.NULL)
        } else if (settings().FORMULAS_KEYWORD.includes(reserved)) {
            return TOKEN(reserved, settings().TOKEN_TYPES.FORMULA)
        } else if (settings().INVERSION_KEYWORD === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.INVERSION)
        } else if (settings().CONJUNCTION_KEYWORD === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.CONJUNCTION)
        } else if (settings().DISJUNCTION_KEYWORD === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.DISJUNCTION)
        } else if (settings().POSITIONAL_ARGUMENT_SEPARATOR === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.POSITIONAL_SEPARATOR) 
        } else if (settings().FUNCTION_KEYWORD === reserved) {
            return TOKEN(reserved, settings().TOKEN_TYPES.FUNCTION)
        } else if (settings().IF_KEYWORDS.includes(reserved)) {
            if (settings().IF_KEYWORDS[0] === reserved) {
                return TOKEN(reserved, settings().TOKEN_TYPES.IF)
            } else {
                return TOKEN(reserved, settings().TOKEN_TYPES.ELSE)
            }
        } else if (settings().BLOCK_KEYWORDS.includes(reserved)) {
            if (settings().BLOCK_KEYWORDS[0] === reserved) {
                return TOKEN(reserved, settings().TOKEN_TYPES.DO)
            } else {
                return TOKEN(reserved, settings().TOKEN_TYPES.END)
            }
        } else {
            return TOKEN(reserved, settings().TOKEN_TYPES.IDENTITY)
        }
    }

    const isReserved = () => {
        return /\w/g.test(expression[position.current]) && expression[position.current].length === 1
    }

    return {
        isReserved,
        getReservedToken
    }
}

const operation = (expression, nextPosition, position) => {
    const getOperationToken = () => {
        let operation = expression[position.current]
        nextPosition()
        while (settings().OPERATION_CHARACTERS.includes(expression[position.current])) {
            operation = operation + expression[position.current]
            nextPosition()
        }
        if (settings().BINARY_OPERATIONS_TO_TOKENS.get(operation) !== undefined) {
            return TOKEN(operation, settings().BINARY_OPERATIONS_TO_TOKENS.get(operation))
        } else {
            throw new errors.SyntaxError(`
            Invalid operation: ${operation}, 
            please use one of the following: ${[...settings().BINARY_OPERATIONS_TO_TOKENS.keys()].join(', ')}
            `)
        }
    }

    const isOperation = () => {
        return settings().OPERATION_CHARACTERS.includes(expression[position.current])
    } 

    return {
        isOperation,
        getOperationToken
    }
}

const string = (expression, nextPosition, position) => {
    const getStringToken = () => {
        let string = ''
        nextPosition()
        while (!isString(expression[position.current])) {
            string = string + expression[position.current]
            nextPosition()
        }
        nextPosition()
        return TOKEN(string, settings().TOKEN_TYPES.STRING)
    }

    const isString = () => {
        return expression[position.current] === settings().STRING_DELIMITER
    }

    return {
        getStringToken,
        isString
    }
}

const number = (expression, nextPosition, position) => {
    const getNumberToken = () => {
        let number = ''
        const decimalPointRegex = new RegExp(`\\${settings().DECIMAL_POINT_CHARACTER}`)
        const isDecimalPoint = () => {
            if (expression[position.current] === settings().DECIMAL_POINT_CHARACTER) {
                if (!decimalPointRegex.test(number)) {
                    return true
                } else {
                    throw new errors.SyntaxError()
                }
            }
            return false
        }
        while (isNumber(expression[position.current]) || isDecimalPoint()) {
            number = number + expression[position.current]
            nextPosition()
        }
        if (decimalPointRegex.test(number)) {
            return TOKEN(number, settings().TOKEN_TYPES.FLOAT)
        } else {
            return TOKEN(number, settings().TOKEN_TYPES.INTEGER)
        }
    }

    const isNumber = () => {
        if (!Number.isNaN(parseInt(expression[position.current])) && expression[position.current] !== ')') {
            return true
        } else {
            return false
        }
    }

    return {
        isNumber,
        getNumberToken
    }
}

const lexer = (expression) => {
    expression = expression.split('')

    const position = {
        current: 0
    }

    const nextPosition = () => {
        position.current++
    }

    const NUMBER = number(expression, nextPosition, position)
    const STRING = string(expression, nextPosition, position)
    const OPERATION = operation(expression, nextPosition, position)
    const RESERVED = reserved(expression, nextPosition, position)

    const isSpace = () => {
        return expression[position.current] === ' '
    }

    /**
     * gets next character without advancing to the next token
     */
    const peekCharacter = (peekChars = 0) => {
        return expression[position.current + peekChars]
    }

    const getNextToken = () => {
        let token = null

        while(isSpace()) {
            nextPosition()
        }
        if (expression[position.current] === undefined) {
            token = TOKEN(null, settings().TOKEN_TYPES.END_OF_FILE)
        } else if (NUMBER.isNumber()) {
            token = NUMBER.getNumberToken()
        } else if (STRING.isString()) {
            token = STRING.getStringToken()
        } else if (OPERATION.isOperation()) {
            token = OPERATION.getOperationToken()
        } else if (RESERVED.isReserved()) {
            token = RESERVED.getReservedToken()
        } else if (expression[position.current] === '\n') {
            token = TOKEN(expression[position.current], settings().TOKEN_TYPES.NEWLINE)
            nextPosition()
        } else if (expression[position.current] === '(') {
            token = TOKEN(expression[position.current], settings().TOKEN_TYPES.LEFT_PARENTHESIS)
            nextPosition()
        } else if (expression[position.current] === ')') {
            token = TOKEN(expression[position.current], settings().TOKEN_TYPES.RIGHT_PARENTHESIS)
            nextPosition()
        } else if (expression[position.current] === settings().POSITIONAL_ARGUMENT_SEPARATOR) {
            token = TOKEN(expression[position.current], settings().TOKEN_TYPES.POSITIONAL_ARGUMENT_SEPARATOR)
            nextPosition()
        } else {
            throw new errors.SyntaxError(`Invalid character: ${expression[position.current]}`)
        }
        return token
    }

    return {
        peekCharacter,
        getNextToken
    }
}

module.exports = lexer