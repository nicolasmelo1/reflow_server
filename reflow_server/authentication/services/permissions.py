class AuthenticationPermissionsService:
    @staticmethod
    def is_valid_compay(company):
        if company and company.is_active:
            return True
        else:
            return False

    @staticmethod
    def is_valid_user_company(company, user):
        if user and company and user.company_id == company.id:
            return True
        else:
            return False
    
    @staticmethod
    def is_valid_admin_only_path(user, url_name):
        """
        Validates if the user is trying to access an admin only path
        """
        from reflow_server.authentication.services.routes import admin_only_url_names

        if url_name in admin_only_url_names:
            if user.profile.name == 'admin':
                return True
            else: 
                return False
        else:
            return True

    @staticmethod
    def is_valid_public_path(url_name):
        from reflow_server.authentication.services.routes import can_be_public_url_names
        if url_name in can_be_public_url_names:
            return True
        else:
            return False
