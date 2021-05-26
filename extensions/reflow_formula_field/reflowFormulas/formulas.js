// DEPRECATED

const Count = (parameters) => {
    return parameters.length
}

const Sum = (parameters) => {
    return parameters.reduce((acumulator, currentValue) => acumulator + currentValue, 0)
}

module.exports = {
    Count,
    Sum
}