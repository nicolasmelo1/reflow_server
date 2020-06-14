from django.urls import URLPattern, URLResolver

# if you want the url names that can be accessed only by admins
admin_only_url_names = list()

# if you want the url names that accepts formulary attachments.
attachment_url_names = list()

def __extract_url(extract_list, url, **kwargs):
    """
    This function is private for this file ONLY, please don't try to extend or to import.
    This extracts based on a recursion, this way we can extract all of the url names even on 
    includes.

    Arguments:
        extract_list {list} -- The list you want to save the url name
        url {django.urls.re_path, django.urls.url} -- The url you want to save to a list

    Returns:
        django.urls.re_path, django.urls.url -- The original url
    """
    if 'original_url' not in kwargs:
        original_url = url
    else:
        original_url = kwargs['original_url']

    # if the url has the parameter `name`, it is probably a re_path or path instance
    # otherwise it is just a list of urls (so a `include`), then we can extract all of the urls names
    # even if it is an include.
    if hasattr(url, 'name'):
        name = url.name
        extract_list.append(name)
    elif isinstance(url, URLResolver):
       for url in url.urlconf_name:
           __extract_url(extract_list, url=url, original_url=original_url)
    return original_url


def register_admin_only_url(url):
    """
    This handy function is used to register admin urls, when you want to register an url only avalable for an admin
    of a company you use this function.

    This extracts the name of the url and appends it to a list so it can be checked and validated later.

    This also works for urls with includes.

    HOW TO USE THIS FUNCTION:
    on your `urls.py`:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_admin_only_url(re_path(r'^protected_url/$', ProtectedView.as_view(), name='protected')),
    ]

    This also works for includes so on your `urls.py` you could do this:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_admin_only_url(
            re_path(r'^formulary/', include([
                re_path(r'^$', jwt_required(validate_payment(validate_permissions(RenderFormulary.as_view()))), name='manage_formulary'),
            ]))
        ),
    ]

    Arguments:
        url {django.urls.re_path, django.urls.url} -- The url you want to protect

    Returns:
        [django.urls.re_path, django.urls.url] -- The original url
    """
    return __extract_url(admin_only_url_names, url)


def register_attachment_url(url):
    """
    This handy function is used to register urls that recieves attachments, this attachments are used to validate 
    how much attachments a user can have with the billing app. 

    This extracts the name of the url and appends it to a list so it can be checked and validated later.

    This also works for urls with includes.

    HOW TO USE THIS FUNCTION:
    on your `urls.py`:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_attachment_url(re_path(r'^protected_url/$', ProtectedView.as_view(), name='protected')),
    ]

    This also works for includes so on your `urls.py` you could do this:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_attachment_url(
            re_path(r'^formulary/', include([
                re_path(r'^$', jwt_required(validate_payment(validate_permissions(RenderFormulary.as_view()))), name='manage_formulary'),
            ]))
        ),
    ]

    Arguments:
        url {[django.urls.re_path, django.urls.url]} -- The url you want to protect

    Returns:
        [django.urls.re_path, django.urls.url] -- The original url
    """
    return __extract_url(attachment_url_names, url)