from django.conf import settings

import requests

class ExternalService:
    @staticmethod
    def is_response_authorized(request):
        """
        Checks if a request is authorized and validated so it can reach the view function.
        We use this to protect all of our requests internally since we transit sensitive information
        between reflow apps.

        Obviously, we only need this on production environment, on development environment the apps
        can communicate freely.

        Arguments:
            request {django.Request} -- The request recieved in a view.

        Returns:
            bool -- returns True or False whether the request is valid or not.
        """
        if settings.ENV == 'server':
            if 'HTTP_AUTHORIZATION' in request.META:
                header = request.META['HTTP_AUTHORIZATION']
                response = requests.get(url=settings.AUTH_BEARER_HOST+'/auth/', headers={'Authorization': header})
                response = response.json()
                if 'status' in response and response['status'] == 'logged':
                    return True
                else:
                    return False
            else:
                return False
        return True
    
    @staticmethod
    def authorize_request():
        """
        This function is used to authorize the request from internal applications of reflow,
        we have a `worker` app and can have many others. So for this we use an external app called `auth-bearer`
        that handles all of the authentication between aplications. With this handy function we can create
        a authorization header for this application for when it tries to connect with other apps.
        """
        if settings.ENV == 'server':
            response = requests.post(settings.AUTH_BEARER_HOST+'/auth/', json={
                'username': settings.APP_NAME,
                'password': settings.SECRET_KEY
            })
            if response.status_code != 200:
                response = requests.post(settings.AUTH_BEARER_HOST+'/auth/', json={
                    'username': settings.AUTH_BEARER_USERNAME,
                    'password': settings.AUTH_BEARER_PASSWORD
                })

                if response.status_code != 200:
                    raise Exception({'msg': 'something happened'})
                else:
                    headers = {"Authorization": "Bearer {}".format(response.json()['access_token'])}
                    response = requests.put(settings.AUTH_BEARER_HOST+'/auth/', json={
                        'username': settings.APP_NAME,
                        'password': settings.SECRET_KEY
                    }, headers=headers)
                    if response.status_code != 200:
                        raise Exception({'msg': 'something happened'})
                    else:
                        return ExternalService.authorize_request()
            else:
                return {"Authorization": "Bearer {}".format(response.json()['access_token'])}
        else:
            return {}

