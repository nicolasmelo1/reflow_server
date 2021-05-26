const object = require('./object.js')
const { INTEGER_TYPE, FLOAT_TYPE, STRING_TYPE, BOOLEAN_TYPE } = require('../types')
const { ValueError } = require('../../errors.js')

class int extends object {
    constructor() {
        super(INTEGER_TYPE)
    }

    __initialize__(value) {
        this.value = parseInt(value)
        return super.__initialize__()
    }

    /**
     * On integers we can only add between Floats or Integers, when adding by an integer, returns an integer, otherwise returns a float.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float, int>} - Returns either a float when multiplying by floats or a int
     */
    __add__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === FLOAT_TYPE) {
            const float = require('./float')
            const response = new float()
            return response.__initialize__(representation + objectRepresentation)
        } else if (object.type === INTEGER_TYPE) {
            const response = new int()
            return response.__initialize__(representation + objectRepresentation)
        } else {
            super.__add__(object)
        }
    }

    /**
     * On integers we can only subtract from another integer or another float, other types are unsuported. When subtracting
     * by an float always return a float.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float, int>} - Returns either a float or a int
     */
    __subtract__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === FLOAT_TYPE) {
            const float = require('./float')
            const response = new float()
            return response.__initialize__(representation - objectRepresentation)
        } else if (object.type === INTEGER_TYPE) {
            const response = new int()
            return response.__initialize__(representation - objectRepresentation)
        } else {
            super.__subtract__(object)
        }
    }

    /**
     * Multiplication with integers are supported between string, float or other ints, all other types are unsuported.
     * When the user multiplies a string with an int we repeat the string n times, returning a new string object,
     * When the user multiplies with a float we return a new float object, as it should be expected.
     * Last but not least when the user multiplies with int we return a new object of type int with the newly created value.
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<string, float, integer>} - Could return an object of type string, int or float, otherwise throws an error.
     */
    __multiply__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            const string = require('./string')
            const response = new string()
            return response.__initialize__(objectRepresentation.repeat(representation))
        } else if (object.type === FLOAT_TYPE) {
            const float = require('./float')
            const response = new float()
            return response.__initialize__(representation * objectRepresentation)
        } else if (object.type === INTEGER_TYPE) {
            const response = new int()
            return response.__initialize__(representation * objectRepresentation)
        } else {
            super.__multiply__(object)
        }
    }

    /**
     * You can either divide by an integer or by a float, also remember, you can't divide by 0
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float, int>} - Returns either a float or a int
     */
    __divide__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()
        
        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            if (parseInt(objectRepresentation) === 0) {
                throw ValueError('Cannot divide by 0')
            } else if (object.type === FLOAT_TYPE) {
                const float = require('./float')
                const response = new float()
                return response.__initialize__(representation / objectRepresentation)
            } else {
                const response = new int()
                return response.__initialize__(representation / objectRepresentation)
            }
        } else {
            super.__divide__(object)
        }
    }

    /**
     * Really similar to add or subtract, power is only available between ints and floats, other types are not supported
     * 
     * @param {object} object - This object can be of many types
     * 
     * @returns {object<float, int>} - Returns the power of either a float or a int
     */
    __power__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()
        
        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            const result = Math.pow(representation, objectRepresentation)
            if (object.type === FLOAT_TYPE && result !== Infinity) {
                const float = require('./float')
                const response = new float()
                return response.__initialize__(result)
            } else if (object.type === INTEGER_TYPE && result !== Infinity) {
                const response = new int()
                return response.__initialize__(result) 
            } else {
                const none = require('./none')   
                const response = new none()
                return response.__initialize__()
            }
        } else {
            super.__power__(object)
        }
    }
    
    /**
     * For truthy or Falsy values in ints, if the value is 0 then it is represented as False, otherwise it is represented
     * as True.
     * 
     * @returns {object<boolean>} - Returns a boolean object representing either True or False
     */
    __boolean__() {
        const representation = this.representation()
        if (representation === 0) {
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
     * @returns {object<int>} - Returns a new int object with the positive value of the number
     */
    __unaryPlus__() {
        const response = new int()
        return response.__initialize__(+this.__representation__())
    }

    /**
     * Returns the negative representation of the particular float number
     * 
     * @returns {object<int>} - Returns a new float object with the negative value of the number
     */
    __unaryMinus__() {
        const response = new int()
        return response.__initialize__(-this.__representation__())
    }

    __getValue__() {

    }

    __representation__() {
        return this.value
    }
}   

module.exports = int