const { settings } = require('../settings')
const { 
    FunctionDefinition,
    FunctionCall,
    Float, 
    Integer, 
    BinaryOperation, 
    String, 
    Boolean, 
    UnaryOperation,
    UnaryConditional,
    BinaryConditional,
    BooleanOperation,
    Null,
    IfStatement,
    Program,
    Block,
    Assign,
    Variable
} = require('./nodes')
const errors = require('../errors')

/**
 * ////////////////////////////////////////////////////////////
 * // This is the Grammar of Reflow Formulas, it is based and inspired
 * // on EBNF grammar: https://pt.wikipedia.org/wiki/Formalismo_de_Backus-Naur_Estendido
 * // 
 * // If you don't know what grammars are read:
 * // https://pt.wikipedia.org/wiki/Formalismo_de_Backus-Naur 
 * //
 * // Basically it is a way of representing a structure of a syntax, every programming language
 * // has one of this. This grammar helps us with the hole logic for the parsing.
 * //
 * // _ABOUT THE PARSER_
 * // The parser uses recursion in order to transverse all of the tokens of the expression. The original article where
 * // this was inspired from (Reference: https://ruslanspivak.com/lsbasi-part7/) uses while loops in order to transverse the
 * // hole structure. I was also using this, but then thought that since it also uses recursion, using ONLY recursion would be easier
 * // to comprehend.
 * ////////////////////////////////////////////////////////////
 * 
 * program: block END_OF_FILE
 * 
 * block: statements_list 
 * 
 * compound_statement: IF if_statement 
 *                      | FUNCTION function_statement
 *  *                     
 * function_statement: FUNCTION IDENTITY LEFT_PARENTHESIS (parameters)?* RIGHT_PARENTHESIS DO block END
 * 
 * function_call: IDENTITY LEFT_PARENTHESIS (expression POSITIONAL_ARGUMENT_SEPARATOR)?* RIGHT_PARENTHESIS
 * 
 * parameters: ((IDENTITY | assignment) POSITIONAL_ARGUMENT_SEPARATOR)*
 * 
 * if_statement: IF expression DO block ((ELSE else_statement)? | END) 
 * 
 * else_statement: (ELSE DO block | ELSE IF if_statement) END
 * 
 * statements_list: (statement NEWLINE)* 
 * 
 * statement: block
 *            | assignment
 *            | empty 
 * 
 * assignment: variable ASSIGN expression
 *              | expression
 * 
 * expression: disjunction
 * 
 * disjunction: (disjunction ((OR) | disjunction)*
 *              | conjunction
 * 
 * conjunction : (conjunction ((AND) | conjunction)*
 *               | inversion
 * 
 * inversion: (NOT) inversion
 *            | comparison
 * 
 * comparison: comparison (( GREATER_THAN | GREATER_THAN_EQUAL | LESS_THAN | LESS_THAN_EQUAL | EQUAL | DIFFERENT) comparison)* 
 *             | sum
 *  
 * sum: sum ((PLUS | MINUS) sum)*
 *       | product
 * 
 * product: product ((MULTIPLACATION | DIVISION | REMAINDER) product)*
 *          | power
 * 
 * power: power ((POWER) power)*
 *        | unary
 * 
 * unary: (SUM | SUBTRACTION) unary
 *      | primary
 * 
 * primary: atom
 *          | IDENTITY LEFT_PARENTHESIS function_call
 *          | primary LEFT_BRACKET atom (COMMA atom)* RIGHT_BRACKET
 * 
 * atom: INTEGER 
 *      | FLOAT 
 *      | STRING
 *      | BOOLEAN
 *      | LEFT_PARENTHESIS disjunction RIGHT_PARENTHESIS
 *      | variable
 *      | function_statement
 *      | LEFT_BRACKET list
 * 
 * list: LEFT_BRACKET expression (COMMA expression)* RIGHT_BRACKET
 * 
 * variable: IDENTITY
 * 
 * @returns {Object} - Returns the Abstract Syntax Tree of the formulas, so we can interpret and evaluate in interpreter function. 
 */
 const parser = (lexer) => {
    const LEXER = lexer
    let currentToken = LEXER.getNextToken()
    
    /**
     * Gets next token validating current token
     */
    const getNextToken = (tokenType) => {
        if (tokenType === currentToken.tokenType) {
            const nextToken = LEXER.getNextToken()
            currentToken = nextToken
        } else {
            throw new errors.SyntaxError(`Expected token: ${tokenType}, current token: ${currentToken.tokenType}`)
        }
    }
    
    const variable = () => {
        return Variable(currentToken)
    }

    /**
     * atom: INTEGER 
     *      | FLOAT 
     *      | STRING
     *      | BOOLEAN
     *      | LEFT_PARENTHESIS disjunction RIGHT_PARENTHESIS
     *      | variable
     *      | function_statement
     */
    const atom = () => {
        const token = currentToken
        const tokenType = currentToken.tokenType
        if (settings().TOKEN_TYPES.IDENTITY === currentToken.tokenType && LEXER.peekCharacter() === '(') {
            return functionCallStatement()
        } else {
            switch (tokenType) {
                case settings().TOKEN_TYPES.BOOLEAN:
                    node = Boolean(token)
                    getNextToken(tokenType)
                    return node
                case settings().TOKEN_TYPES.INTEGER:
                    node = Integer(token)
                    getNextToken(tokenType)
                    return node
                case settings().TOKEN_TYPES.NULL:
                    node = Null()
                    getNextToken(tokenType)
                    return node
                case settings().TOKEN_TYPES.STRING:
                    node = String(token)
                    getNextToken(tokenType)
                    return node
                case settings().TOKEN_TYPES.FLOAT:
                    node = Float(token)
                    getNextToken(tokenType)
                    return node
                case settings().TOKEN_TYPES.LEFT_PARENTHESIS:
                    getNextToken(tokenType)
                    node = disjunction()
                    getNextToken(settings().TOKEN_TYPES.RIGHT_PARENTHESIS)
                    return node
                case settings().TOKEN_TYPES.IDENTITY:
                    node = variable()
                    getNextToken(tokenType)
                    return node
            }
        }
    }

    /**
     * unary: (SUM | SUBTRACTION) unary
     *       | atom
     */
    const unary = () => {
        if ([
            settings().TOKEN_TYPES.SUM,
            settings().TOKEN_TYPES.SUBTRACTION,
        ].includes(currentToken.tokenType)) {
            const operation = currentToken
            getNextToken(currentToken.tokenType)
            const value = unary()
            return UnaryOperation(operation, value)
        } else {
            return atom()
        }
    }

    /**
     * power: power ((POWER) power)*
     *        | unary
     */
    const power = () => {
        let node = unary()

        if (settings().TOKEN_TYPES.POWER === currentToken.tokenType) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = product()
            return BinaryOperation(left, right, operation)
        } else {
            return node
        }
    }
    /**
     * product: product ((MULTIPLACATION | DIVISION | REMAINDER) product)*
     *          | power
     */
    const product = () => {
        let node = power()

        if ([
            settings().TOKEN_TYPES.DIVISION, 
            settings().TOKEN_TYPES.REMAINDER, 
            settings().TOKEN_TYPES.MULTIPLICATION
        ].includes(currentToken.tokenType)) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = product()
            return BinaryOperation(left, right, operation)
        } else {
            return node
        }
    }
    
    /**
     * sum: sum ((PLUS | MINUS) sum)*
     *       | product
     */
    const sum = () => {
        let node = product()

        if ([
            settings().TOKEN_TYPES.SUM, 
            settings().TOKEN_TYPES.SUBTRACTION
        ].includes(currentToken.tokenType)) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = sum()
            return BinaryOperation(left, right, operation)
        } else {
            return node
        }
    }

    /**
     * comparison: comparison (( GREATER_THAN | GREATER_THAN_EQUAL | LESS_THAN | LESS_THAN_EQUAL | EQUAL | DIFFERENT) comparison)* 
     *             | sum
     */
    const comparison = () => {
        let node = sum()
        if ([
            settings().TOKEN_TYPES.GREATER_THAN, 
            settings().TOKEN_TYPES.GREATER_THAN_EQUAL,
            settings().TOKEN_TYPES.DIFFERENT,
            settings().TOKEN_TYPES.LESS_THAN,
            settings().TOKEN_TYPES.LESS_THAN_EQUAL,
            settings().TOKEN_TYPES.EQUAL
        ].includes(currentToken.tokenType)) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = comparison()
            if (left === undefined || right === undefined) {
                throw new errors.SyntaxError()
            }
            return BinaryConditional(left, right, operation)
        } else {
            return node
        }
    }

    /**
     * inversion: INVERSION inversion
     *            | comparison
     */
    const inversion = () => {
        let node = comparison()

        if (settings().TOKEN_TYPES.INVERSION === currentToken.tokenType) {
            const operation = currentToken
            getNextToken(currentToken.tokenType)
            const value = inversion()
            if (value === undefined) {
                throw new errors.SyntaxError(`You forgot to close the 'not' operator`)
            }
            return UnaryConditional(operation, value)
        } else {
            return node
        }
    }
    
    /**
     * conjunction : (conjunction ((AND) | conjunction)*
     *               | inversion
     */
    const conjunction = () => {
        let node = inversion()

        if (settings().TOKEN_TYPES.CONJUNCTION === currentToken.tokenType) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = conjunction()
            if (left === undefined || right === undefined) {
                throw new errors.SyntaxError("Ops, looks like you forgot to finish the 'and' expression")
            }
            return BooleanOperation(node, right, operation)
        } else {
            return node
        }
    }

    /**
     * disjunction: (disjunction ((OR) | disjunction)*
     *              | conjunction
     */
    const disjunction = () => {
        let node = conjunction()

        if (settings().TOKEN_TYPES.DISJUNCTION === currentToken.tokenType) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = disjunction()
            if (left === undefined || right === undefined) {
                throw new errors.SyntaxError("Ops, looks like you forgot to finish the 'or' expression")
            }
            return BooleanOperation(left, right, operation)
        } else {
            return node
        }
    }

    /**
     * expression: disjunction
     */
    const expression = () => {
        let node = disjunction()
        return node
    }

    /**
     * assignment: variable ASSIGN expression
     *              | expression
     */
    const assignment = () => {
        let node = expression()

        if (settings().TOKEN_TYPES.ASSIGN === currentToken.tokenType) {
            const operation = currentToken
            const left = node
            getNextToken(currentToken.tokenType)
            const right = expression()
            if (left.nodeType !== settings().NODE_TYPES.VARIABLE) {
                throw new errors.SyntaxError("Cannot assign, needs to assign value to a variable")
            } else if (right === undefined) {
                throw new errors.SyntaxError("You forgot to assign a value to a variable")
            }
            return Assign(left, right, operation)
        } else {
            return node
        }
    }
    /* 
    * statement: compoundStatement
    *            | assignment
    *            | empty 
    **/
    const statement = () => {
        let node = compoundStatement()
        if (node) {
            return node
        } else {
            return assignment()
        }
    }

    /**
     * else_statement: (ELSE DO block | ELSE IF if_statement) END
     */
    const elseStatement = () => {
        if (settings().TOKEN_TYPES.ELSE === currentToken.tokenType) {
            getNextToken(settings().TOKEN_TYPES.ELSE)
            if (settings().TOKEN_TYPES.IF === currentToken.tokenType) {
                return ifStatement()
            } else {
                getNextToken(settings().TOKEN_TYPES.DO)
                const node = block() 
                getNextToken(settings().TOKEN_TYPES.END)
                return node
            }
        }
    }

    /**
     * parameters: (IDENTITY assignment (POSITIONAL_ARGUMENT_SEPARATOR assignment)*)?
     */
    const parameters = (parametersList=[]) => {
        if (settings().TOKEN_TYPES.IDENTITY === currentToken.tokenType) {
            const node = assignment()
            parametersList.push(node)
            if (settings().TOKEN_TYPES.POSITIONAL_ARGUMENT_SEPARATOR === currentToken.tokenType) {
                getNextToken(settings().TOKEN_TYPES.POSITIONAL_ARGUMENT_SEPARATOR)
                return parameters(parametersList)
            } else {
                return parametersList
            }
        }
    }

    /*
     * function_statement: FUNCTION IDENTITY LEFT_PARENTHESIS (parameters)?* RIGHT_PARENTHESIS DO block END
     **/
    const functionStatement = () => {
        if (settings().TOKEN_TYPES.FUNCTION === currentToken.tokenType) {
            getNextToken(settings().TOKEN_TYPES.FUNCTION)
            const functionVariable = variable()
            getNextToken(settings().TOKEN_TYPES.IDENTITY)
            getNextToken(settings().TOKEN_TYPES.LEFT_PARENTHESIS)
            let parametersList = []
            if (settings().TOKEN_TYPES.IDENTITY === currentToken.tokenType) {
                parametersList = parameters()
            } 
            getNextToken(settings().TOKEN_TYPES.RIGHT_PARENTHESIS)
            getNextToken(settings().TOKEN_TYPES.DO)
            const functionBlock = block()
            getNextToken(settings().TOKEN_TYPES.END)
            return FunctionDefinition(functionVariable, parametersList, functionBlock)
        }
    }

    /**
     * function_call: IDENTITY LEFT_PARENTHESIS (expression POSITIONAL_ARGUMENT_SEPARATOR)?* RIGHT_PARENTHESIS
     */
    const functionCallStatement = (functionName=null, functionArguments=[]) => {
        if (functionName === null) {
            functionName = currentToken.value
            getNextToken(settings().TOKEN_TYPES.IDENTITY)
            getNextToken(settings().TOKEN_TYPES.LEFT_PARENTHESIS)
        }
        if (settings().TOKEN_TYPES.RIGHT_PARENTHESIS !== currentToken.tokenType) {
            const argument = expression()
            functionArguments.push(argument)
            if (settings().TOKEN_TYPES.POSITIONAL_ARGUMENT_SEPARATOR === currentToken.tokenType) {
                getNextToken(settings().TOKEN_TYPES.POSITIONAL_ARGUMENT_SEPARATOR)
            }
            return functionCallStatement(functionName, functionArguments)
        } else {
            getNextToken(settings().TOKEN_TYPES.RIGHT_PARENTHESIS)
            return FunctionCall(functionName, functionArguments)
        }
    }

    /**
     * if_statement: IF expression DO block ((ELSE else_statement)? | END) 
     */
    const ifStatement = () => {
        if (settings().TOKEN_TYPES.IF === currentToken.tokenType) {
            getNextToken(settings().TOKEN_TYPES.IF)
            let expr = expression()
            getNextToken(settings().TOKEN_TYPES.DO)
            let blck = block()
            let elseStmt = null
            if (currentToken.tokenType === settings().TOKEN_TYPES.ELSE) {
                elseStmt = elseStatement()
            } else {
                getNextToken(settings().TOKEN_TYPES.END)
            }
            return IfStatement(expr, blck, elseStmt)
        }
    }
    
    const compoundStatement = () => {
        if (settings().TOKEN_TYPES.IF === currentToken.tokenType) {
            return ifStatement()
        } else if (settings().TOKEN_TYPES.FUNCTION === currentToken.tokenType) {
            return functionStatement()
        }
    }
    
    /**
     * statement_list: (statement NEWLINE)*
     */
    const statementsList = (instructions = []) => {
        let node = statement()
        if (node) {
            instructions.push(node)
        }
        if (settings().TOKEN_TYPES.NEWLINE === currentToken.tokenType) { 
            getNextToken(currentToken.tokenType)
            return statementsList(instructions)
        } else {
            return instructions
        }
    }

    /**
     * block: statements_list 
     *        | definitions
     */
    const block = () => {
        const instructions = statementsList()
        return Block(instructions)
    }

    /**
     * program: block END_OF_FILE
     */
    const program = () => {
        const block_node = block()
        const program_node = Program(block_node)
        if (currentToken.tokenType !== settings().TOKEN_TYPES.END_OF_FILE) {
            throw SyntaxError('Unexpected end of file, this means your program cannot be executed and was ended abruptly')
        }
        
        return program_node
    }
    /**
     * Starts at `disjunction`
     * 
     * @returns {Object} - This Object will be the Abstract Syntax Tree of the hole formula structure.
     * It doesn't have a default structure since every node has it's own structure, but for example,
     * this simple formula: 
     * 1 + 2 - 3 and 3 + 5 + 0
     * 
     * will be translated to this:
     * {
     *   "nodeType": "BOOLEAN_OPERATION",
     *   "left": {
     *       "nodeType": "BINARY_OPERATION",
     *       "left": {
     *           "nodeType": "INTEGER",
     *           "token": {
     *               "value": "1",
     *               "tokenType": "INTEGER"
     *           },
     *           "value": "1"
     *       },
     *       "right": {
     *           "nodeType": "BINARY_OPERATION",
     *           "left": {
     *               "nodeType": "INTEGER",
     *               "token": {
     *                   "value": "2",
     *                   "tokenType": "INTEGER"
     *               },
     *               "value": "2"
     *           },
     *           "right": {
     *               "nodeType": "INTEGER",
     *               "token": {
     *                   "value": "3",
     *                   "tokenType": "INTEGER"
     *               },
     *               "value": "3"
     *           },
     *           "operation": {
     *               "value": "-",
     *               "tokenType": "SUBTRACTION"
     *           }
     *       },
     *       "operation": {
     *           "value": "+",
     *           "tokenType": "SUM"
     *       }
     *   },
     *   "right": {
     *       "nodeType": "BINARY_OPERATION",
     *       "left": {
     *           "nodeType": "INTEGER",
     *           "token": {
     *               "value": "3",
     *               "tokenType": "INTEGER"
     *           },
     *           "value": "3"
     *       },
     *       "right": {
     *           "nodeType": "BINARY_OPERATION",
     *           "left": {
     *               "nodeType": "INTEGER",
     *               "token": {
     *                   "value": "5",
     *                   "tokenType": "INTEGER"
     *               },
     *               "value": "5"
     *           },
     *           "right": {
     *               "nodeType": "INTEGER",
     *               "token": {
     *                   "value": "0",
     *                   "tokenType": "INTEGER"
     *               },
     *               "value": "0"
     *           },
     *           "operation": {
     *               "value": "+",
     *               "tokenType": "SUM"
     *           }
     *       },
     *       "operation": {
     *           "value": "+",
     *           "tokenType": "SUM"
     *       }
     *   },
     *   "operation": {
     *       "value": "and",
     *       "tokenType": "CONJUNCTION"
     *   }
     *}
     */
    const parse = () => {
        const node = program()
        return node
    }

    return parse()
}

module.exports = parser