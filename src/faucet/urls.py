from django.urls import path
from .api.views import fund_api, stats_api


urlpatterns = [
    path('fund', fund_api, name='fund'),
    path('stats', stats_api, name='stats'),
]
