def is_integer(value):
    try:
        value = int(value)
        return True
    except:
        return False

def is_string(value):
    return isinstance(value, str)

def is_boolean(value):
    return isinstance(value, bool)

def is_float(value):
    try:
        value = float(value)
        return True
    except:
        return False
