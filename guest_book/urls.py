from django.conf.urls import url

from . import views
app_name = "guest_book"

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^members/$', views.members, name = "members"),
    url(r'^members/(?P<member_id>[0-9]+)', views.member_detail, name = "detail"),
    ]
