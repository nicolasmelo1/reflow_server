from reflow_server.core.utils.routes import extract_url

# if you want the url names that accepts formulary attachments.
attachment_url_names = list()

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
    return extract_url(attachment_url_names, url)