const object = require('./object.js')
const { BOOLEAN_TYPE, FLOAT_TYPE, INTEGER_TYPE } = require('../types')

class boolean extends object {
    constructor() {
        super(BOOLEAN_TYPE)
    }

    __initialize__(value) {
        this.value = value
        return super.__initialize__()
    }

    __boolean__() {
        return this
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
        let representation = this.__representation__()
        representation = representation ? 1 : 0
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
        let representation = this.__representation__()
        representation = representation ? 1 : 0
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
        let representation = this.__representation__()
        representation = representation ? 1 : 0
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
        let representation = this.__representation__()
        representation = representation ? 1 : 0
        let objectRepresentation = object.__representation__()

        if ([FLOAT_TYPE, INTEGER_TYPE].includes(object.type)) {
            return super.newBoolean(representation >= objectRepresentation)
        } else if (object.type === BOOLEAN_TYPE) {
            objectRepresentation = objectRepresentation ? 1 : 0
            return super.newBoolean(representation >= objectRepresentation)
        }
        return super.__greaterThanEqual__(object)
    }

    /**
     * On a boolean, when you write +True, it works like if True was equal 1
     * it gives you 1 and if it is +False it is 0
     * 
     * @returns {object<int>} - Returns a new int object with the value 0 or 1
     */
    __unaryPlus__() {
        const int = require('./int')
        const response = new int()
        if (this.__representation__() === true) {
            return response.__initialize__(1)
        } else {
            return response.__initialize__(0)
        }
    }

    /**
     * On a boolean, when you write -True, it works like if True was equal 1
     * it gives you -1 and if it is -False it is 0
     * 
     * @returns {object<int>} - Returns a new int object with the value 0 or -1
     */
    __unaryMinus__() {
        const int = require('./int')
        const response = new int()
        if (this.__representation__() === true) {
            return response.__initialize__(-1)
        } else {
            return response.__initialize__(0)
        }
    }

    __getValue__() {

    }

    __representation__() {
        return Boolean(this.value)
    }
}   


module.exports = boolean