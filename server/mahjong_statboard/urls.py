"""mahjong_statboard URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_nested import routers

from mahjong_statboard import views


router = routers.DefaultRouter()
router.register(r'instances', views.InstancesViewSet)

instances_router = routers.NestedDefaultRouter(router, r'instances', lookup='instance')
instances_router.register(r'games', views.GamesViewSet, base_name='games')
instances_router.register(r'players', views.PlayersViewSet, base_name='players')
instances_router.register(r'ratings', views.RatingsViewSet, base_name='ratings')
instances_router.register(r'stats', views.StatsViewSet, base_name='stats')
instances_router.register(r'meetings', views.MeetingsViewSet, base_name='meetings')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/', include(router.urls + instances_router.urls)),
    url(r'^api/instances/(?P<instance_id>[0-9]+)/games_csv/', views.GamesListCsv.as_view())
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

