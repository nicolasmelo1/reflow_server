from django.conf.urls import re_path, include

from reflow_server.analytics.views import TrackView, SurveyView

urlpatterns = [
    re_path(r'^survey/(?P<survey_id>\d+)/$', SurveyView.as_view(), name='survey_view'),
    re_path(r'^track/(?P<event_name>[\w_]+)/$', TrackView.as_view(), name='analytics_track')
]