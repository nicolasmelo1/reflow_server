
############################################################################################
class DraftPublicPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, draft_string_id=None):
        self.draft_string_id = draft_string_id
        self.company_id = company_id
    # ------------------------------------------------------------------------------------------

    def __call__(self, request):
        pass
    # ------------------------------------------------------------------------------------------
