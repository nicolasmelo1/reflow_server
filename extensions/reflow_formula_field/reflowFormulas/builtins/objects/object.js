/**
 * This is an object, it represents every object of reflow formulas.
 * Every object, similarly to python will contain some double underscore (or dunder) methods.
 * 
 * Those dunder methods are responsible for handling common behaviour in the program like equals, difference, sum, multiplication,
 * and so on.
 * 
 * The idea is that by doing this we take away much of the complexity and the workload of the interpreter function
 * and give more power to the builtin object types so they are able to handle itself.
 * 
 * With this we are able to create stuff like 'Hello world'.length (this .length can be a function we call on a atribute of the string type)
 * we are able to give more funcionality to the integer, strings, floats and so on.
 * 
 * Okay, so how does this work?
 * 
 * When the interpreter finds a binary operation for example (1 + 2) 
 * what we do is valueLeft.__add__(valueRight). Super simple. If you understand right, 1 will be represented
 * as an object `int(1)`, so in other words, the REAL value is `int(1).__add__(int(2))`.
 * 
 * That's the kind of flexibility and achievment we can have by doing stuff like this.
 * 
 * OKAY, but what happens to the ORIGINAL value?
 * 
 * The original value can be retrieved by calling __representation__(): this is the JS value or the value in whatever language you are using to
 * build this interpreter on.
 */
class object {
    constructor(type) {
        this.type = type
    }

    newBoolean(value) {
        const boolean = require('./boolean')
        const response = new boolean()
        return response.__initialize__(value)
    }

    __initialize__() {
        return this
    }

    __add__(object) {
        throw SyntaxError(`Unsuported operation '+' between types ${this.type} and ${object.type}`)
    }

    __subtract__(object) {
        throw SyntaxError(`Unsuported operation '-' between types ${this.type} and ${object.type}`)
    }

    __multiply__(object) {
        throw SyntaxError(`Unsuported operation '*' between types ${this.type} and ${object.type}`)
    }

    __divide__(object) {
        throw SyntaxError(`Unsuported operation '/' between types ${this.type} and ${object.type}`)
    }

    __power__(object) {
        throw SyntaxError(`Unsuported operation '^' between types ${this.type} and ${object.type}`)
    }

    __equals__(object) {        
        const TRUE = this.newBoolean(true)
        const FALSE = this.newBoolean(false)

        if (object.type === this.type && object.__representation__() === this.__representation__()) {
            return TRUE.__boolean__()
        } else {
            return FALSE.__boolean__()
        }
    }

    __difference__(object) {
        const TRUE = this.newBoolean(true)
        const FALSE = this.newBoolean(false)

        if (object.type !== this.type || object.__representation__() !== this.__representation__()) {
            return TRUE.__boolean__()
        } else {
            return FALSE.__boolean__()
        }
    }

    __lessThan__(object) {
        return this.newBoolean(false)
    }

    __lessThanEqual__(object) {
        const isEquals = this.__equals__(object) 
        
        if (isEquals.__boolean__().__representation__() === true) {
            return this.newBoolean(true)
        } else {
            return this.newBoolean(false)
        }
    }

    __greaterThan__(object) {        
        return this.newBoolean(false)
    }

    __greaterThanEqual__(object) {
        const isEquals = this.__equals__(object) 
        
        if (isEquals.__boolean__().__representation__() === true) {
            return this.newBoolean(true)
        } else {
            return this.newBoolean(false)
        }
    }

    /**
     * __boolean__ should ALWAYS return a boolean object, if any other type is returned, a error is thrown.
     */
    __boolean__() {
        return this.newBoolean(false)
    }

    __not__() {
        return this.newBoolean(!this.__boolean__().__representation__())
    }

    __and__(object) {
        return this.newBoolean(this.__boolean__().__representation__() && object.__boolean__().__representation__())
    }

    __or__(object) {
        return this.newBoolean(this.__boolean__().__representation__() || object.__boolean__().__representation__())
    }

    __unaryPlus__() {
        throw SyntaxError(`Unsuported operand type + for ${this.type}`)
    }

    __unaryMinus__() {
        throw SyntaxError(`Unsuported operand type - for ${this.type}`)
    }

    __getValue__() {}

    __representation__() {
        return this
    }
}   

module.exports = object