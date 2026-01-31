from django.urls import path
from .views import HPDBProxyView, UserSettingsProxyView, AppConfigProxyView

urlpatterns = [
    path('hpdb/<path:path>', HPDBProxyView.as_view()),
    path('hpdb/', HPDBProxyView.as_view()),
    path('usersettings/<path:path>', UserSettingsProxyView.as_view()),
    path('usersettings/', UserSettingsProxyView.as_view()),
    path('appconfig/<path:path>', AppConfigProxyView.as_view()),
    path('appconfig/', AppConfigProxyView.as_view()),
]
