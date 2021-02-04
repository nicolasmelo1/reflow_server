rate_limiting_cache = {}


class RateLimiting:
    def __init__(self, request):
        user_ip = self.get_client_ip(request)  
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.token = str(hash(user_ip + user_agent))
        self.path = request.META.get('PATH_INFO', '') + request.META.get('QUERY_STRING', '')
        rate_limiting_cache[self.token] = rate_limiting_cache.get(self.token, []) + [self.path]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self):
        if len([path for path in rate_limiting_cache.get(self.token, []) if path == self.path]) > 3 :
            return True
        else:
            return False

    def clean(self):
        rate_limiting_cache[self.token].remove(self.path)
        