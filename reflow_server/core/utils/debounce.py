import time
import threading

def debounce(wait, callback=None):
    """ 
    Decorator that will postpone a functions execution until after wait seconds
    have elapsed since the last time it was invoked. 
     
    This is more common in the JS world to just submit the information when the user
    has stopped typing but it can also be useful on the backend for caching and prevent
    multiple updates at the same time.
    
    Args:
        wait (int): The number of seconds to wait before executing the function 
        callback (function | None): A callback function to execute after wait seconds for further verification, 
                                    if None, the function will be executed
    """

    def decorator(function):
        def debounced(*args, **kwargs):
            def call_function():
                debounced._timer = None
                debounced._last_call = time.time()
                return function(*args, **kwargs)

            time_since_last_call = time.time() - debounced._last_call
            if time_since_last_call >= wait:
                is_callback_defined = callback is not None
                if is_callback_defined:
                    if callback(*args, **kwargs):  
                        return call_function()
                else:
                    return call_function()
                    
            if debounced._timer is None:
                debounced._timer = threading.Timer(wait - time_since_last_call, call_function)
                debounced._timer.start()

        debounced._timer = None
        debounced._last_call = 0

        return debounced

    return decorator