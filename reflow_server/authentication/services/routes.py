from reflow_server.core.utils.routes import extract_url


# if you want the url names that can be accessed only by admins
admin_only_url_names = list()

# url names that can be public and exposed
can_be_public_url_names = list()

# ------------------------------------------------------------------------------------------
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
    return extract_url(admin_only_url_names, url)
# ------------------------------------------------------------------------------------------
def register_can_be_public_url(url):
    """
    This handy function is used to register admin urls, when you want to register an url only avalable for an admin
    of a company you use this function.

    This extracts the name of the url and appends it to a list so it can be checked and validated later.

    This also works for urls with includes.

    HOW TO USE THIS FUNCTION:
    on your `urls.py`:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_can_be_public_url(re_path(r'^protected_url/$', ProtectedView.as_view(), name='protected')),
    ]

    This also works for includes so on your `urls.py` you could do this:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_can_be_public_url(
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
    return extract_url(can_be_public_url_names, url)