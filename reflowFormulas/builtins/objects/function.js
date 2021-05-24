const object = require('./object.js')
const { FUNCTION_TYPE } = require('../types')

class functions extends object {
    constructor() {
        super(FUNCTION_TYPE)
    }

    __initialize__(astFunction, scope, parameters) {
        this.scope = scope
        this.astFunction = astFunction
        this.parameters = parameters
        return super.__initialize__()
    }
}

module.exports = functions