const object = require('./object.js')
const { FLOAT_TYPE, INTEGER_TYPE } = require('../types')

class float extends object {
    constructor() {
        super(FLOAT_TYPE)
    }

    __initialize__(value) {
        this.value = value
        return super.__initialize__()
    }

    /**
     * Similar to subtraction always return a float if you are either adding by int or float
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float>} - Returns always a float when working with floats
     */
    __add__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            const response = new float()
            return response.__initialize__(representation + objectRepresentation)
        } else {
            super.__add__(object)
        }
    }

    /**
     * Similar to Multiply and Divide, always return a float if you are either subtracting by int or float
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float>} - Returns always a float when working with floats
     */
    __subtract__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            const response = new float()
            return response.__initialize__(representation - objectRepresentation)
        } else {
            super.__subtract__(object)
        }
    }

    /**
     * You can either multiply by an integer or by a float.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float>} - Returns always a float when working with floats
     */
    __multiply__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            const response = new float()
            return response.__initialize__(representation * objectRepresentation)
        } else {
            super.__multiply__(object)
        }
    }

     /**
     * You can either divide by an integer or by a float, also remember, you can't divide by 0. Always return a float.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float>} - Returns always a float when working with floats
     */
    __divide__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            if (parseInt(objectRepresentation) === 0) {
                throw ValueError('Cannot divide by 0')
            } else {
                const response = new float()
                return response.__initialize__(representation / objectRepresentation)
            }
        } else {
            super.__divide__(object)
        }
    }

    /**
     * Similar to add, subtract, and others, always returns a float and can be either done between Floats or Integers.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float>} - Returns a float with the power of both values
     */
    __power__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            const response = new float()
            return response.__initialize__(Math.pow(representation, objectRepresentation))
        } else {
            super.__power__(object)
        }
    }

    /**
     * Really similar to int boolean. The truthy or falsy works basically the same, when the value is 0.0 or 0.00 or whatever
     * we convert this value representation to integer and checks if it's 0, if it is then it's false, otherwise it's true.
     *  
     * @returns {object<boolean>} - Returns a boolean value representing either True or either False
     */
    __boolean__() {
        const representation = this.__representation__()
        if (parseInt(representation) === 0) {
            return super.newBoolean(false)
        } else {
            return super.newBoolean(true)
        }
    }

    /**
     * When it's less than we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
     * compare to float or int.
     * 
     * @param {object} object - This object can be of any type
     * 
     * @returns {object<boolean>} - Returns a boolean object representing either True or False for the less than conditional. 
     */
     __lessThan__(object) {
        const representation = this.__representation__()
        let objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            return super.newBoolean(representation < objectRepresentation)
        } else if (object.type === BOOLEAN_TYPE) {
            objectRepresentation = objectRepresentation ? 1 : 0
            return super.newBoolean(representation < objectRepresentation)
        }
        return super.__lessThan__(object)
    }

    /**
     * When it's less than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
     * compare to float or int.
     * 
     * @param {object} object - This object can be of any type
     * 
     * @returns {object<boolean>} - Returns a boolean object representing either True or False for the less than equal conditional. 
     */
    __lessThanEqual__(object) {
        const representation = this.__representation__()
        let objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            return super.newBoolean(representation <= objectRepresentation)
        } else if (object.type === BOOLEAN_TYPE) {
            objectRepresentation = objectRepresentation ? 1 : 0
            return super.newBoolean(representation <= objectRepresentation)
        }
        return super.__lessThanEqual__(object)
    }

    /**
     * When it's grater than we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
     * compare to float or int.
     * 
     * @param {object} object - This object can be of any type
     * 
     * @returns {object<boolean>} - Returns a boolean object representing either True or False for the greater than conditional. 
     */
    __greaterThan__(object) {
        const representation = this.__representation__()
        let objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            return super.newBoolean(representation > objectRepresentation)
        } else if (object.type === BOOLEAN_TYPE) {
            objectRepresentation = objectRepresentation ? 1 : 0
            return super.newBoolean(representation > objectRepresentation)
        }
        return super.__greaterThan__(object)
    }

    /**
     * When it's greater than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
     * compare to float or int.
     * 
     * @param {object} object - This object can be of any type
     * 
     * @returns {object<boolean>} - Returns a boolean object representing either True or False for the greater than equal conditional. 
     */
     __greaterThanEqual__(object) {
        const representation = this.__representation__()
        let objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            return super.newBoolean(representation > objectRepresentation)
        } else if (object.type === BOOLEAN_TYPE) {
            objectRepresentation = objectRepresentation ? 1 : 0
            return super.newBoolean(representation > objectRepresentation)
        }
        return super.__greaterThan__(object)
    }

    /**
     * Returns the positive representation of the particular number
     * 
     * @returns {object<float>} - Returns a new float object with the positive value of the number
     */
    __unaryPlus__() {
        const response = new float()
        return response.__initialize__(+this.__representation__())
    }

    /**
     * Returns the negative representation of the particular float number
     * 
     * @returns {object<float>} - Returns a new float object with the negative value of the number
     */
    __unaryMinus__() {
        const response = new float()
        return response.__initialize__(-this.__representation__())
    }

    __getValue__() {}

    __representation__() {
        return this.value * 1.0
    }
}   

module.exports = float