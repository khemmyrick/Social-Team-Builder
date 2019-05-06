from projects import views


# Create your views here.
def home(request):
    return views.ProjectList.as_view(request)