const object = require('./object.js')
const { NONE_TYPE } = require('../types')

class none extends object {
    constructor() {
        super(NONE_TYPE)
    }

    __initialize__() {
        this.value = null
        return super.__initialize__()
    }

    __representation__() {
        return this.value
    }
}   

module.exports = none