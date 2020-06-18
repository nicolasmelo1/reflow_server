"""reflow_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('reflow_server.core.urls'), name='core_app'),
    url(r'^billing/', include('reflow_server.billing.urls'), name='billing_app'),
    url(r'^authentication/', include('reflow_server.authentication.urls'), name='authentication_app'),
    url(r'^formula/', include('reflow_server.formula.urls'), name='formula_app'),
    url(r'^notification/', include('reflow_server.notification.urls'), name='notification_app'),
    url(r'^kanban/', include('reflow_server.kanban.urls'), name='kanban_app'),
    url(r'^listing/', include('reflow_server.listing.urls'), name='listing_app'),
    url(r'^formulary/', include('reflow_server.formulary.urls'), name='formulary_app'),
    url(r'^data/', include('reflow_server.data.urls'), name='data_app'),
    url(r'^theme/', include('reflow_server.theme.urls'), name='theme_app')
]
