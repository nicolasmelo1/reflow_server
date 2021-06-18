/**
 * Manages memory inside of my interpreter.
 * 
 * This memory is responsible for holding all of the variables that the user can use, when we define a function
 * 
 * What we do is send a record object to the scope of the function.
 * 
 * 
 * Okay so we have to concepts on this memory function, those are: Records and CallStack, what's the difference between both?
 * 
 * - Records are a HashMap (in JS this can be translated as an object) containing a the keys and within each key the actual value
 * That's how we are able to access variables, define x=2 and then call x returning it's actual value.
 * - CallStack is different, it holds all of the records, understand each record as the scope of where this variable are running, so if
 * we define x inside of a variable it CAN'T be accessed outside of the scope. CallStack is each scope that is running, when we start a program
 * we create the first scope (record), that is used for the hole program, then when we call a function we have the scope of the function with the variables
 * of this particular function.
 * In other words, the callstack is everything that is running in the moment, probably for multithreading and other stuff you might need to
 * change how this memory is managed and handled.
 */
const memory = () => {
    const record = (name, type) => {
        let nestingLevel = 0
        const members = {}

        const assign = (key, value) => {
            members[key] = value
        }

        const get = (key) => {
            return members[key]
        }

        const setNestingLevel = (level) => {
            nestingLevel = level
        }

        const getNestingLevel = () => {
            return nestingLevel
        }


        return {
            name,
            type,
            getNestingLevel,
            setNestingLevel,
            get,
            assign,
            members
        }
    }

    const callStack = () => {
        const records = []
        
        const pushToCurrent = (record) => {
            records.splice(records.length - 1, 1, record)
        }

        const push = (record) => {
            record.setNestingLevel(records.length)
            if (records.length < 600) {
                records.push(record)
            } else {
                throw Error('Stack is full, this means you are calling too many functions at once, try optimizing your code')
            }
        }
        
        const pop = () => {
            records.pop()
        }

        const peek = () => {
            return records[records.length - 1]
        }

        return {
            push, pop, peek, records, pushToCurrent
        }
    }

    const stack = callStack()

    return {
        record,
        stack
    }
}

module.exports = memory