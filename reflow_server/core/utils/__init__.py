from django.conf import settings


def replace_dumb_characters_from_str(string_to_strip):
    """
    Replaces some characters that could't be cleaned automatically from the string so there are no problems when saving the data. 
    This function is used primarly for creating form_names or field_names, since the string must be a URL friendly string.

    Arguments:
        string_to_strip {str} -- the name of the variable says it all

    Returns:
        str -- the cleaned string
    """
    return string_to_strip.replace(' ', '').replace('´', '').replace('ˆ', '').replace('…', '').replace('˜', '').replace('`', '')


def secure_url(string):
    """
    In production sometimes you want to change unsafe urls for safe urls so it can be showed to the user without the browser 
    trigerring some warning, so it only change http:// to https:// protocol.
   
    Arguments:
        string {str} -- the url you want to secure

    Returns:
        str -- the secured url
    """
    if settings.SECURE_URL:
        return string.replace('http://', 'https://')
    else:
        return string