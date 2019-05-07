from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r"login/$", views.LogInView.as_view(), name="login"),
    url(r"logout/$", views.LogOutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUpView.as_view(), name="signup"),
    url(r'(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name='details'),
    # url(r'(?P<pk>\d+)/edit/$', views.ProfileUpdateView.as_view(), name='edit'),
    url(r'(?P<pk>\d+)/edit/$', views.profile_update_view, name='edit'),
    # url(r'(?P<pk>\d+)/applications/$', views.ApplicationsView.as_view(), name='applications'),
]
