/**
 * Verifies if a given value is an integer value
 * 
 * @param {Any} value - The value to verify if it's a integer
 * 
 * @returns {Boolean} - Returns true if it is a integer and false if not.
 */
const isInteger = (value) => {
    try {
        value = parseInt(value)
        return !['', null, undefined].includes(value) && Number.isInteger(value)
    } catch {
        return false
    }
}

/**
 * Verifies if a given value is a boolean value, so if they are either 'false' or 'true'. If they are we return true, otherwise, false.
 * 
 * @param {Any} value - The value to verify if it's a boolean
 * 
 * @returns {Boolean} - Returns true if it is a boolean and false if not.
 */
const isBoolean = (value) => {
    if (typeof value === "boolean") {
        return true
    } else {
        return false
    }
}

/**
 * Verifies if a given value is a string value. So this means a variable is actually a text.
 * 
 * @param {Any} value - The value to verify if it's a string
 * 
 * @returns {Boolean} - Returns true if it is a string and false if not.
 */
const isString = (value) => {
    if (typeof value === 'string' || value instanceof String) {
        return true
    } else {
        return false
    }
}

/**
 * Verifies if a given value is a float value, so it has decimal point
 * 
 * @param {Any} value - The value to verify if it's a float
 * 
 * @returns {Boolean} - Returns true if it is a Float and false if not.
 */
const isFloat = (value) => {
    try {
        value = parseFloat(value)
        return value
    } catch {
        return false
    }
}

/**
 * In javascript a null can be either undefined or null. In our programming language we have just one representation for empty values: None.
 * So this means, if it's null or undefined it is a null.
 * 
 * @param {Any} value - The value to verify if it's null
 * 
 * @returns {Boolean} - Returns true if it is a null and false if not.
 */
const isNull = (value) => {
    if ([null, undefined].includes(value)) {
        return true
    } else {
        return false
    }
}

module.exports = {
    isString,
    isFloat,
    isBoolean,
    isNull,
    isInteger
}