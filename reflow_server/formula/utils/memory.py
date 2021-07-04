class Record:
    def __init__(self, name, record_type):
        """
        As you probably have guessed, on Memory you will see an explanation on how the CallStack works.
        But you might ask yourself. Okay, but what are each row?

        Each row is called a record. a Record is exactly this class.

        It have a name and a type, is it a function? Is it a method? Is it the program?
        And the name is the name of the function, or program, or whatever. It is just an identifier.

        Besides that you will see we have 'members', what are those?
        Members is exactly the variables, this is where we save the Objects of the reflow_server.formula.utils.builtins.objects.Object object.

        Args:
            name (str): The name of the Record, this is just an identifier, multiple records can have the same name (this happens in a recursion)
            record_type (str): The type of the record, at the time of the writing this can be either PROGRAM or FUNCTION
        """
        self.name = name
        self.record_type = record_type
        self.__nesting_level = 0
        self.members = {}
    # ------------------------------------------------------------------------------------------
    def assign(self, key, value):
        """
        Assigns a new variable with a key, we are storing it in a dict, in other words: Be aware, we can have
        ONE and ONLY ONE variable with an identifier name.

        In this example:
        >>> value = 2
        the key is 'value'. And the value is a reflow_server.formula.utils.builtins.objects.Integer.Integer
        object.

        Args:
            key (str): The key to save this variable to. 
            value (reflow_server.formula.utils.builtins.objects.*): One of the builtin objects generally
        """
        self.members[key] = value
    # ------------------------------------------------------------------------------------------
    def get(self, key):
        """
        Retrieves the variable data. From this example:

        >>> value = 2
        >>> value

        when we do 'value' we actually are referencing to the value 2.

        Args:
            key (str): The key you want to retrieve this is the name of the variable usually.

        Returns:
            reflow_server.formula.utils.builtins.objects.*: Generally one of the following
        """
        try:
            return self.members[key]
        except Exception as e:
            raise Exception('{} was not defined'.format(key))
    # ------------------------------------------------------------------------------------------
    def set_nesting_level(self, nesting_level):
        self.__nesting_level = nesting_level
    # ------------------------------------------------------------------------------------------
    def get_nesting_level(self):
        return self.__nesting_level
############################################################################################
class CallStack:
    """
    This is explained better in Memory class, but you've got it.

    This holds all of the records and it is simple as this. It's just a list that we use to hold all of the records
    """
    def __init__(self):
        self.records = []
    # ------------------------------------------------------------------------------------------
    def push_to_current(self, record):
        """
        For Tail Call Optimization when a Tail Recursion Call is made we push the next record to the current record, not filling 
        the hole call stack.

        You might want to read here: https://en.wikipedia.org/wiki/Tail_call

        Args:
            record (reflow_server.formula.utils.memory.Record): The record object to add as the last item in the call stack

        Returns:
            reflow_server.formula.utils.memory.Record: Returns the added Record object.
        """
        self.records[len(self.records) - 1] = record
        return record
    # ------------------------------------------------------------------------------------------
    def push(self, record):
        """
        Similar to `.push_to_current()` except that this fills the CallStack.

        Args:
            record (reflow_server.formula.utils.memory.Record): The record object to add as the last item in the call stack

        Raises:
            Exception: When you've added too many items in the callstack it raises an error.

        Returns:
            reflow_server.formula.utils.memory.Record: Returns the added Record object.
        """
        record.set_nesting_level(len(self.records))
        if len(self.records) < 99:
            self.records.append(record)
        else:
            raise Exception('Stack is full, this means you are calling too many functions at once, try optimizing your code')
        return record
    # ------------------------------------------------------------------------------------------
    def pop(self):
        """
        Removes the latest added record from the callstack.

        Returns:
            reflow_server.formula.utils.memory.Record: Returns the removed Record object.
        """
        return self.records.pop()
    # ------------------------------------------------------------------------------------------
    def peek(self):
        """
        Peeks to see the latest added Record from the callstack, with this we can get all of the variables and identities.

        Returns:
            reflow_server.formula.utils.memory.Record: Returns the removed Record object.
        """
        return self.records[len(self.records) - 1]
############################################################################################
class Memory:
    """
    This is the memory. It is a virtual memory, of course not the actual hardware memory in the computer.

    The idea is super super simple: The memory controls the CallStack.
    OH, You've never learned about CallStack? Okay i will try to explain.

    Let's program in python for the sake of this example, so suppose the following code:

    >>> def subtraction(a, b):
            return a - b

    >>> def sum(a, b):
            return a + b

    >>> print(subtraction(2,1))
        print(sum(1,2))

    What happens when we do this? Yup, it prints 1 and 3, you've got it.
    But how this works under the hood?

    1º:
    -------------------------------------------------------------------------------------------- 
    | Nesting Lv   || Record Name  || Variables                 || Values                      |   
    -------------------------------------------------------------------------------------------- 
    |  0           || PROGRAM      || sum ; subtraction         || function ; function         |
    -------------------------------------------------------------------------------------------- 

    2º:
    -------------------------------------------------------------------------------------------- 
    | Nesting Lv   || Record Name  || Variables                 || Values                      |   
    -------------------------------------------------------------------------------------------- 
    |  0           || PROGRAM      || sum ; subtraction         || function ; function         |
    |  1           || subtraction  || sum ; subtraction ; a ; b || function ; function ; 2 ; 1 |
    -------------------------------------------------------------------------------------------- 

    3º:
    -------------------------------------------------------------------------------------------- 
    | Nesting Lv   || Record Name  || Variables                 || Values                      |   
    -------------------------------------------------------------------------------------------- 
    |  0           || PROGRAM      || sum ; subtraction         || function ; function         |
    |  1           || sum          || sum ; subtraction ; a ; b || function ; function ; 1 ; 2 |
    -------------------------------------------------------------------------------------------- 

    4º:
    -------------------------------------------------------------------------------------------- 
    | Nesting Lv   || Record Name  || Variables                 || Values                      |   
    -------------------------------------------------------------------------------------------- 
    |  0           || PROGRAM      || sum ; subtraction         || function ; function         |
    -------------------------------------------------------------------------------------------- 

    "WHAT THE HELL?"

    So what does it do? First we start the program, when we start the program we add this hole script to the call stack.
    Understand the program as the "GLOBAL". You know global variables and all that stuff? This is what the Program holds, all
    variables available fo the hole program to use.

    Okay, so what comes next? This program will hold the variables sum and subtraction, understand 'sum' as a string
    and 'subtraction' as a string. Both strings are keys of dictionary, and both 'sum' and 'subtraction' are functions.

    it's something like:
    >>> {
        'sum': lambda a, b: a + b,
        'subtraction': lambda a, b: a - b
    }

    Okay so what happens next is that first we call 'subtraction' function, this function is added to the call stack, the value 
    is returned and then it is poped from the call stack (we've already used the function)

    The same happens when we call 'sum', the function is added to the call stack, all the variables from the previous record become
    available for us to use inside of the function and we enable 'a' and 'b' for usage.

    This might sound too complex, but it's not

    >>> x = 2
    def sum(a):
        return a + x
    print(a)

    What happens when we run this?
    It gives an error, right, can you point where?

    Exactly, on `print(a)`. But Why?? Because the variable 'a' is available ONLY inside of the function when the function is running.
    But why "a + x" works? Exacly, because everything from the outer scope is available inside of the function.

    Okay, so let's continue: notice how a and b only exists while the sum and 'subtraction' are running, but when they are removed, both
    variables doesn't exist anymore.

    That's the hole idea of the call stack, the call stack is a stack (FILO (first in, last out)) as the name suggests, so whatever
    is at the BOTTOM of the stack is the record we are in. In the 3º phase look that 'sum' is in the last position of the stack
    so this is what is being runned at the moment.

    When we finish running this we remove this from the stack and go back to the latest record from the stack.

    With this information, can you understand how a recursion works?
    """
    def __init__(self):
        self.stack = CallStack()
        