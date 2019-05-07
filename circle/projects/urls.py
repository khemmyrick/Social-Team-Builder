from django.conf.urls import url

from . import views

app_name = 'projects'
urlpatterns = [
    # url(r'new/$', views.CreateProjectView.as_view(), name='new'),
    url(r'search/$', views.ProjectListView.as_view(), name='search'),
    url(r'(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='details'),
    # url(r'(?P<pk>\d+)/edit/$', views.ProjectEditView.as_view(), name='edit'),
    # url(r'(?P<pk>\d+)/delete/$', views.ProjectDeleteView.as_view(), name='delete'),
]

# project search might just be main project index page.
# search view goes here. list view goes to main project index. 
# no pk necessary. context info will handle that.