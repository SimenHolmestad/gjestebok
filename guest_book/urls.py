from django.conf.urls import url

from . import views
from .views import MemberCreate
app_name = "guest_book"

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^members/$', views.members, name = "members"),
    url(r'^entries/$', views.Entries.as_view() , name = "entries"),
    url(r'^entries/edit/(?P<pk>[0-9]+)/$', views.EditEntry.as_view(), name = "edit_entry"),
    url(r'^entries/delete/(?P<pk>[0-9]+)/$', views.EntryDelete.as_view(), name = "delete_entry"),
    url(r'^new_entry/$', views.NewEntry.as_view(), name = "new_entry"),
    url(r'^members/(?P<member_id>[0-9]+)', views.member_detail, name = "member_detail"),
    url(r'^members/new_member/$', MemberCreate.as_view(), name = "new_member"),
    url(r'^members/edit/(?P<member_id>[0-9]+)/$', views.edit_member, name = "edit_member"),
    url(r'^members/delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name = "delete_member"),
    ]
