from django.conf import settings


class AnalyticsService:
    def __init__(self, user_id):
        settings.MIXPANEL.track()

