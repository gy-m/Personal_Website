from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    # path('', views.index, {'pagename': '', 'project_name': ''}, name='home'),     # create parameter named pagename, init it with '' and pass it to the view  
    path('', views.index, {'pagename': ''}, name='home'),                           # create parameter named pagename, init it with '' and pass it to the view  
    path('<str:project_permalink>', views.projects, name='projects'),                    # capture every thing after the domain name and send it as a parameter to the view (name of the parameter is project_name)
    path('<str:pagename>', views.index, name='index'),                              # capture every thing after the domain name and send it as a parameter to the view (name of the parameter is pagename)

    # path('<str:pagename><str:project_name>', views.projects, name='projects'),    # if the view supports 2 parameters, this is the right order
]