from django.conf.urls import url

from . import views

app_name = 'projects'
urlpatterns = [
    # url(r'new/$', views.CreateProjectView.as_view(), name='new'),
    # url(r'search/$', views.CreateProjectView.as_view(), name='search'),
    # url(r'(?P<pk>\d+)/$', views.ProjectView.as_view(), name='project'),
    # url(r'(?P<pk>\d+)/edit/$', views.ProjectEditView.as_view(), name='edit'),
]

# project search might just be main project index page.
# search view goes here. list view goes to main project index. 
# no pk necessary. context info will handle that.