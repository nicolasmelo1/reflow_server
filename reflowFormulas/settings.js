const formulas = require('./formulas')

let context = {
    keywords: {
        conjunction: 'and',
        disjunction: 'or',
        inversion: 'not',
        null: 'None',
        boolean: {
            true: 'True',
            false: 'False'
        },
        if: {
            if: 'if',
            else: 'else'
        }, 
        block: {
            do: 'do',
            end: 'end'
        },
        function: 'function',
        decimal_point_separator: ',',
        positional_argument_separator: ';'
    },
    formulas: {
        'count': formulas.Count,
        'sum': formulas.Sum
    }
}

const setContext = (_context) => {
    if (_context !== undefined) {
        if (_context.keywords !== undefined) {
            if (_context.keywords.boolean !== undefined) {
                context.keywords.boolean = {
                    ...context.keywords.boolean,
                    ..._context.keywords.boolean
                }
            }
            context.keywords = {
                ...context.keywords,
                ..._context.keywords,

            }
        }
        if (_context.formulas !== undefined) {
            context.formulas = {
                ...context.formulas,
                ..._context.formulas
            }
        }
    }
}

const settings = () => {
    const NODE_TYPES = {
        PROGRAM: 'PROGRAM',
        IF_STATEMENT: 'IF_STATEMENT',
        BINARY_OPERATION: 'BINARY_OPERATION',
        BINARY_CONDITIONAL: 'BINARY_CONDITIONAL',
        INTEGER: 'INTEGER',
        FORMULA: 'FORMULA',
        FLOAT: 'FLOAT',
        STRING: 'STRING',
        BOOLEAN: 'BOOLEAN',
        NULL: 'NULL',
        UNARY_OPERATION: 'UNARY_OPERATION',
        UNARY_CONDITIONAL: 'UNARY_CONDITIONAL',
        BOOLEAN_OPERATION: 'BOOLEAN_OPERATION',
        BLOCK: 'BLOCK',
        ASSIGN: 'ASSIGN',
        VARIABLE: 'VARIABLE',
        FUNCTION_DEFINITION: 'FUNCTION_DEFINITION',
        FUNCTION_CALL: 'FUNCTION_CALL'
    }

    const TOKEN_TYPES = {
        ASSIGN: 'ASSIGN',
        INTEGER: 'INTEGER',
        FLOAT: 'FLOAT',
        BOOLEAN: 'BOOLEAN',
        FORMULA: 'FORMULA',
        POSITIONAL_SEPARATOR: 'POSITIONAL_SEPARATOR',
        STRING: 'STRING',
        FUNCTION: 'FUNCTION',
        LEFT_PARENTHESIS: 'LEFT_PARENTHESIS',
        RIGHT_PARENTHESIS: 'RIGHT_PARENTHESIS',
        GREATER_THAN_EQUAL: 'GREATER_THAN_EQUAL',
        LESS_THAN_EQUAL: 'LESS_THAN_EQUAL',
        NOT: 'NOT',
        NULL: 'NULL',
        DIFFERENT: 'DIFFERENT',
        LESS_THAN: 'LESS_THAN',
        GREATER_THAN: 'GREATER_THAN',
        DIVISION: 'DIVISION', 
        REMAINDER: 'REMAINDER', 
        SUBTRACTION: 'SUBTRACTION', 
        SUM: 'SUM',
        MULTIPLICATION: 'MULTIPLICATION',
        POWER: 'POWER', 
        EQUAL: 'EQUAL',
        INVERSION: 'INVERSION',
        DISJUNCTION: 'DISJUNCTION',
        CONJUNCTION: 'CONJUNCTION',
        END_OF_FILE: 'END_OF_FILE',
        NEWLINE: 'NEWLINE',
        IDENTITY: 'IDENTITY',
        DO: 'DO',
        END: 'END',
        IF: 'IF',
        ELSE: 'ELSE',
        FUNCTION: 'FUNCTION',
        POSITIONAL_ARGUMENT_SEPARATOR: 'POSITIONAL_ARGUMENT_SEPARATOR'
    }

    const FORMULAS = context.formulas

    const FORMULAS_KEYWORD = Object.keys(FORMULAS)

    const POSITIONAL_ARGUMENT_SEPARATOR = context.keywords.positional_argument_separator
    const NULL_KEYWORD = context.keywords.null
    const FUNCTION_KEYWORD = context.keywords.function
    const BLOCK_KEYWORDS = [context.keywords.block.do, context.keywords.block.end]
    const IF_KEYWORDS = [context.keywords.if.if, context.keywords.if.else]
    const BOOLEAN_KEYWORDS = [context.keywords.boolean.true, context.keywords.boolean.false]
    const CONJUNCTION_KEYWORD = context.keywords.conjunction
    const DISJUNCTION_KEYWORD = context.keywords.disjunction
    const INVERSION_KEYWORD = context.keywords.inversion
    const RESERVED_KEYWORDS = [...BOOLEAN_KEYWORDS, ...FORMULAS_KEYWORD, CONJUNCTION_KEYWORD, DISJUNCTION_KEYWORD, INVERSION_KEYWORD, POSITIONAL_ARGUMENT_SEPARATOR]

    const DECIMAL_POINT_CHARACTER = context.keywords.decimal_point_separator
    const STRING_DELIMITER = '"'

    const OPERATION_CHARACTERS = ['>' ,'<', '=', '!', '/', '+', '*', '%', '-', '^']

    const BINARY_OPERATIONS_TO_TOKENS = new Map([
        [`${OPERATION_CHARACTERS[0]}${OPERATION_CHARACTERS[2]}`, TOKEN_TYPES.GREATER_THAN_EQUAL],
        [`${OPERATION_CHARACTERS[1]}${OPERATION_CHARACTERS[2]}`, TOKEN_TYPES.LESS_THAN_EQUAL],
        [`${OPERATION_CHARACTERS[3]}${OPERATION_CHARACTERS[2]}`, TOKEN_TYPES.DIFFERENT],
        [`${OPERATION_CHARACTERS[0]}`, TOKEN_TYPES.GREATER_THAN],
        [`${OPERATION_CHARACTERS[1]}`, TOKEN_TYPES.LESS_THAN],
        [`${OPERATION_CHARACTERS[4]}`, TOKEN_TYPES.DIVISION],
        [`${OPERATION_CHARACTERS[7]}`, TOKEN_TYPES.REMAINDER],
        [`${OPERATION_CHARACTERS[8]}`, TOKEN_TYPES.SUBTRACTION],
        [`${OPERATION_CHARACTERS[5]}`, TOKEN_TYPES.SUM],
        [`${OPERATION_CHARACTERS[9]}`, TOKEN_TYPES.POWER],
        [`${OPERATION_CHARACTERS[6]}`, TOKEN_TYPES.MULTIPLICATION],
        [`${OPERATION_CHARACTERS[2]}${OPERATION_CHARACTERS[2]}`, TOKEN_TYPES.EQUAL],
        [`${OPERATION_CHARACTERS[2]}`, TOKEN_TYPES.ASSIGN]
    ])
    return {
        FUNCTION_KEYWORD,
        RESERVED_KEYWORDS,
        BOOLEAN_KEYWORDS,
        FORMULAS_KEYWORD,
        FORMULAS,
        IF_KEYWORDS,
        BLOCK_KEYWORDS,
        POSITIONAL_ARGUMENT_SEPARATOR,
        NULL_KEYWORD,
        CONJUNCTION_KEYWORD,
        DISJUNCTION_KEYWORD,
        INVERSION_KEYWORD,
        BINARY_OPERATIONS_TO_TOKENS,
        OPERATION_CHARACTERS,
        STRING_DELIMITER,
        DECIMAL_POINT_CHARACTER,
        TOKEN_TYPES,
        NODE_TYPES
    }
}

module.exports = {
    setContext,
    settings
}
