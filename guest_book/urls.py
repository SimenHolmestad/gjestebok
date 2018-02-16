from django.conf.urls import url

from . import views
app_name = "guest_book"

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    ]
