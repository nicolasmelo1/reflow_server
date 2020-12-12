from django.urls import URLPattern, URLResolver


def extract_url(extract_list, url, **kwargs):
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
           extract_url(extract_list, url=url, original_url=original_url)
    return original_url
