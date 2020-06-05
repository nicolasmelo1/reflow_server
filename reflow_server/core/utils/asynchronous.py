import threading
from django.conf import settings

semaphore = threading.BoundedSemaphore(
    value=settings.ASYNC_RESPONSE_MAXIMUM_CONCURRENCY_THREADS)


class RunAsyncFunction(threading.Thread):
    def __init__(self, callback, **kwargs):
        """
        You can run your function with `.delay()` and send all of the parameters of the function using the `.delay()` method

        MOTIVATION:
            This app IS NOT async, but sometimes you might face the need to run some bound heavy tasks, and for it using
            celery might be like killing an ant with a bazooka.
            So if you want to run some heavy tasks in the background before sending the response to the client, use this class.
            It's important to notice that you don't care about the results of the functions that you run here. Also, you don't care
            about monitoring.

        IMPORTANT:
            USE THIS AS LAST RESORT, THIS DOESN'T PROVIDE ANY MONITORING OR EXCEPTION HANDLING, RETRY ON FAILURE, RETURN, ETC. 
            FOR THAT YOU MIGHT WANT TO USE CELERY, SO ALWAYS TRY TO COME UP WITH A SOLUTION USING THE `REFLOW_WORKER` APPLICATION INSTEAD

        Arguments:
            callback {function} -- the function to be run.
        """
        self.callback = callback
        super().__init__(**kwargs)

    def run(self):
        if not hasattr(self, 'callback_parameters'):
            msg = 'You must call `.delay()` to run your function'
            raise AssertionError(msg)
        # semaphore is used so we can limit the maximum number of concurrent threads
        # after the function has run we release this thread so there is room for another threads
        # to be run.
        semaphore.acquire()
        try:
            self.callback(**self.callback_parameters)
        finally:
            semaphore.release()

    def start(self):
        if not hasattr(self, 'callback_parameters'):
            msg = 'You must call `.delay()` to run your function'
            raise AssertionError(msg)
        super(RunAsyncFunction, self).start()

    def delay(self, **kwargs):
        """
        Call this method to run your function and send your arguments of your function on this function
        """
        self.callback_parameters = kwargs
        self.start()