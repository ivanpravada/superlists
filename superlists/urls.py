from django.conf.urls import include
from django.urls import re_path
from lists import views as list_views
from lists import urls as list_urls
from lists import api_urls
# from lists.api import router
from accounts import urls as accounts_urls

urlpatterns = [
    re_path(r'^$', list_views.home_page, name='home'),
    re_path(r'^lists/', include(list_urls)),
    re_path(r'^accounts/', include(accounts_urls)),
    re_path(r'^api/', include(api_urls)),
    # re_path(r'^api/', include(router.urls)),
]
