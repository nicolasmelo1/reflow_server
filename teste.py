import time
import threading
import asyncio
import random 

when_notification_was_generated_by_company_id = {}

def debounce_generate_notification_execution():
    """ 
    Decorator that will postpone a functions execution until after wait seconds
    have elapsed since the last time it was invoked. 
     
    This is more common in the JS world to just submit the information when the user
    has stopped typing but it can also be useful on the backend for caching and prevent
    multiple updates at the same time.
    
    Reference: https://gist.github.com/walkermatt/2871026
    
    Args:
        wait (int): The number of seconds to wait before executing the function 
        callback (function | None): A callback function to execute after wait seconds for further verification, 
                                    if None, the function will be executed
    """

    def decorator(function):
        def debounced(*args, **kwargs):
            company_id = kwargs.get('company_id', None)
            company_id = company_id if company_id is not None and len(args) >= 2 else args[1]
            WAIT_TIME_IN_SECONDS = 10
            
            
            if company_id not in when_notification_was_generated_by_company_id:
                when_notification_was_generated_by_company_id[company_id] = dict(
                    last_call_at=time.time(),
                    timer=None
                )
            debounce_cache_data_of_company_id = when_notification_was_generated_by_company_id[company_id]
            
            def call_function():
                debounce_cache_data_of_company_id['timer'] = None
                debounce_cache_data_of_company_id['last_call_at'] = time.time()
                return function(*args, **kwargs)

            time_since_last_call_by_company_id = time.time() - debounce_cache_data_of_company_id['last_call_at']
            if time_since_last_call_by_company_id > WAIT_TIME_IN_SECONDS:
                debounce_cache_data_of_company_id['timer'].cancel()
                call_function()
            else:
                is_to_cancel_last_timer_by_company_id = debounce_cache_data_of_company_id['timer'] is not None
                if is_to_cancel_last_timer_by_company_id:
                    debounce_cache_data_of_company_id['timer'].cancel()
                
                when_to_call_function = WAIT_TIME_IN_SECONDS - time_since_last_call_by_company_id
                when_to_call_function = when_to_call_function if when_to_call_function > 0 else 0
                debounce_cache_data_of_company_id['timer'] = threading.Timer(when_to_call_function, call_function)
                debounce_cache_data_of_company_id['timer'].start()

        when_notification_was_generated_by_company_id = {}
        return debounced

    return decorator


class PreNotificationService:
    @debounce_generate_notification_execution()
    def create_and_update_pre_notifications(self, company_id):
        print('--------------')
        print('>>>create_and_update_pre_notifications<<<', company_id)
        print('--------------')
        

def simulate_real_app(company_id):
    pre_notification_service_test = PreNotificationService()
    print('simulate_real_app', company_id)
    pre_notification_service_test.create_and_update_pre_notifications(company_id)
        
def main():
    random_company_ids = [1111, 2222]
    for i in range(20):
        company_id = random_company_ids[random.randint(0, len(random_company_ids) - 1)]
        time.sleep(1)
        simulate_real_app(company_id)

main()