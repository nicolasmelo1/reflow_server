class Record:
    def __init__(self, name, record_type):
        self.name = name
        self.record_type = record_type
        self.__nesting_level = 0
        self.members = {}
    
    def assign(self, key, value):
        self.members[key] = value
    
    def get(self, key):
        return self.members.get(key, None)

    def set_nesting_level(self, nesting_level):
        self.__nesting_level = nesting_level
    
    def get_nesting_level(self):
        return self.__nesting_level


class CallStack:
    def __init__(self):
        self.records = []
    
    def push_to_current(self, record):
        self.records[len(self.records) - 1] = record
        return record

    def push(self, record):
        record.set_nesting_level(len(self.records))
        if len(self.records) < 99:
            self.records.append(record)
        else:
            raise Exception('Stack is full, this means you are calling too many functions at once, try optimizing your code')
        return record

    def pop(self):
        return self.records.pop()

    def peek(self):
        return self.records[len(self.records) - 1]


class Memory:
    def __init__(self):
        self.stack = CallStack()
        