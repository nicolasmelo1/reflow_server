function SyntaxError (message='invalid syntax') {
    this.message = message
    this.name = 'SyntaxError'
}

function ValueError (message='invalid value') {
    this.message = message
    this.name = 'ValueError'
}

module.exports = {
    SyntaxError, 
    ValueError
}