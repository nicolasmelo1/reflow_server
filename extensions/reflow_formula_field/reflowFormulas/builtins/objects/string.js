const object = require('./object.js')
const { STRING_TYPE, INTEGER_TYPE  } = require('../types')

class string extends object {
    constructor() {
        super(STRING_TYPE)
    }

    __initialize__(value) {
        this.value = value
        return super.__initialize__()
    }

    /**
     * When the other value is a string we concatenate the strings.
     * 
     * @param {object} object - Can recieve an object of any type
     * 
     * @returns {object<string>} - Returns a new string object with concatenated values
     */
    __add__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            const response = new string()
            return response.__initialize__(representation.concat(objectRepresentation))
        } else {
            super.__add__(object)
        }
    }

    /**
     * Similar to int multiplication but the other way around, when the user multiplies a string by an integer we repeat
     * the string n times returning a new integer.
     * 
     * @param {object<any>} object - Can recieve an object of any type
     * 
     * @returns {object<string>} - Either returns a string object or throws an error.
     */
    __multiply__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === INTEGER_TYPE) {
            const response = new string()
            return response.__initialize__(representation.repeat(objectRepresentation))
        } else {
            return super.__multiply__(object)
        }
    }


    __lessThan__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            return super.newBoolean(representation.length < objectRepresentation.length)
        } else {
            return super.__lessThan__(object)
        }
    }

    __lessThanEqual__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            return super.newBoolean(representation.length <= objectRepresentation.length)
        } else {
            return super.__lessThanEqual__(object)
        }
    }

    __greaterThan__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            return super.newBoolean(representation.length > objectRepresentation.length)
        } else {
            return super.__greaterThan__(object)
        }
    }

    __greaterThanEqual__(object) {
        const representation = this.__representation__()
        const objectRepresentation = object.__representation__()

        if (object.type === STRING_TYPE) {
            return super.newBoolean(representation.length >= objectRepresentation.length)
        } else {
            return super.__greaterThanEqual__(object)
        }
    }

    /**
     * When the string is empty, on a boolean operation it is represented as False, otherwise it is represented as true
     * 
     * This is what we can do to have Truthy or Falsy values in the string.
     * 
     * @returns {object<boolean>} - returns a boolean object representing either True or False
     */
    __boolean__() {
        const representation = this.__representation__()
        if (representation === '') {
            return super.newBoolean(false)
        } else {
            return super.newBoolean(true)
        }
    }

    __getValue__() {

    }

    __representation__() {
        return this.value.toString()
    }
}   

module.exports = string