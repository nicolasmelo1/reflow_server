"""reflow_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from reflow_server import automation
from django.urls import re_path, include
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^core/', include('reflow_server.core.urls'), name='core_app'),
    re_path(r'^dashboard/', include('reflow_server.dashboard.urls'), name='dashboard_app'),
    re_path(r'^billing/', include('reflow_server.billing.urls'), name='billing_app'),
    re_path(r'^analytics/', include('reflow_server.analytics.urls'), name='analytics_app'),
    re_path(r'^automation/', include('reflow_server.automation.urls'), name='automation_app'),
    re_path(r'^authentication/', include('reflow_server.authentication.urls'), name='authentication_app'),
    re_path(r'^filter/', include('reflow_server.filter.urls'), name='filter_app'),
    re_path(r'^formula/', include('reflow_server.formula.urls'), name='formula_app'),
    re_path(r'^notification/', include('reflow_server.notification.urls'), name='notification_app'),
    re_path(r'^kanban/', include('reflow_server.kanban.urls'), name='kanban_app'),
    re_path(r'^notify/', include('reflow_server.notify.urls'), name='notify_app'),
    re_path(r'^listing/', include('reflow_server.listing.urls'), name='listing_app'),
    re_path(r'^formulary/', include('reflow_server.formulary.urls'), name='formulary_app'),
    re_path(r'^data/', include('reflow_server.data.urls'), name='data_app'),
    re_path(r'^theme/', include('reflow_server.theme.urls'), name='theme_app'),
    re_path(r'^rich_text/', include('reflow_server.rich_text.urls'), name='rich_text_app'),
    re_path(r'^draft/', include('reflow_server.draft.urls'), name='draft_app'),
    re_path(r'^pdf_generator/', include('reflow_server.pdf_generator.urls'), name='pdf_generator_app'),
]
