from reflow_server.core.utils.routes import extract_url

# This is for the billing permission of pdf generator. This way we can know exactly what url 
# needs to be checked for billing.
pdf_generator_generate_url_name = list()

def register_pdf_generator_generate_url_name(url):
    """
    This handy function is used to register the url that is used to generated pdfs, when you want to register an url that will be used
    to validate if the user can download a new pdf you use this function.

    This extracts the name of the url and appends it to a list so it can be checked and validated later.

    This also works for urls with includes.

    HOW TO USE THIS FUNCTION:
    on your `urls.py`:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_pdf_generator_generate_url_name(re_path(r'^protected_url/$', ProtectedView.as_view(), name='protected')),
    ]

    This also works for includes so on your `urls.py` you could do this:
    >>> urlpatterns = [
        re_path(r'^healthcheck/$', HealthCheck.as_view(), name='health_check'),
        register_pdf_generator_generate_url_name(
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
    return extract_url(pdf_generator_generate_url_name, url)

