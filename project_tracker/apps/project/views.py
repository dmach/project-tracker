# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from models import ProjectGroup
from models import Project


class ProjectGroupListView(ListView):

    model = ProjectGroup
    slug_field = "short"
    template_name = "projectgroup_list.html"
    context_object_name = "project_group_list"


class ProjectGroupDetailView(DetailView):

    model = ProjectGroup
    slug_field = "short"
    template_name = "projectgroup_detail.html"
    context_object_name = "project_group"


class ProjectDetailView(DetailView):

    model = Project
    slug_field = "short"
    template_name = "project_detail.html"
    context_object_name = "project"
