"""project_tracker URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from apps.project.views import ProjectGroupListView, ProjectGroupDetailView
from apps.project.views import ProjectDetailView


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # project group
    url(r'^g/$', ProjectGroupListView.as_view(), name='project-group/list'),
    url(r'^g/(?P<slug>[-\w]+)/$', ProjectGroupDetailView.as_view(), name='project-group/detail'),

    # project
    url(r'^p/(?P<project_group>[-\w]+)/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(), name='project/detail'),
]
