from .select import ThemeSelectService

class ThemeService:
    @staticmethod
    def select_theme(theme_id, company_id, user_id):
        return ThemeSelectService(theme_id, company_id, user_id).select()