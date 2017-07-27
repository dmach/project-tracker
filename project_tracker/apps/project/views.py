# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import ProjectGroup
from .models import Project

import csv, time


class ProjectGroupListView(ListView):

    model = ProjectGroup
    slug_field = "short"
    template_name = "projectgroup_list.html"
    context_object_name = "project_group_list"

    def render_to_response(self, context, **response_kwargs):
        """
        Creates a CSV response if requested, otherwise returns the default
        template response.
        """
        # Sniff if we need to return a CSV export
        if self.request.GET.get('format', '') == 'csv':
            group_list = self.get_queryset()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="projects-%s.csv"' % (time.strftime("%Y-%m-%d"))
            writer = csv.writer(response)
            writer.writerow(['short', 'name', 'owner'])
            for project in group_list:
                writer.writerow([project.short, project.name, project.owner])
            return response
        else:
            return super(ProjectGroupListView, self).render_to_response(context, **response_kwargs)


class ProjectGroupDetailView(DetailView):

    model = ProjectGroup
    slug_field = "short"
    template_name = "projectgroup_detail.html"
    context_object_name = "project_group"

    def render_to_response(self, context, **response_kwargs):
        """
        Creates a CSV response if requested, otherwise returns the default
        template response.
        """
        # Sniff if we need to return a CSV export
        if self.request.GET.get('format', '') == 'csv':
            response = HttpResponse(content_type='text/csv')
            group = self.get_object()
            response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"' % (group.short, time.strftime("%Y-%m-%d"))
            projects = group.project_set.all()
            writer = csv.writer(response)
            writer.writerow(['short', 'name', 'owner', 'description', 'is closed'])
            for item in projects:
                writer.writerow([item.short, item.name, item.owner, item.description, item.is_closed])
            return response
        else:
            return super(ProjectGroupDetailView, self).render_to_response(context, **response_kwargs)


class ProjectDetailView(DetailView):

    model = Project
    slug_field = "short"
    template_name = "project_detail.html"
    context_object_name = "project"

    def render_to_response(self, context, **response_kwargs):
        """
        Creates a CSV response if requested, otherwise returns the default
        template response.
        """
        # Sniff if we need to return a CSV export
        if self.request.GET.get('format', '') == 'csv':
            response = HttpResponse(content_type='text/csv')
            group = self.get_object()
            response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"' % (group.short, time.strftime("%Y-%m-%d"))
            projects = group.project_set.all()
            writer = csv.writer(response)
            writer.writerow(['short', 'name', 'owner', 'description', 'is closed'])
            for item in projects:
                writer.writerow([item.short, item.name, item.owner, item.description, item.is_closed])
            return response
        else:
            return super(ProjectDetailView, self).render_to_response(context, **response_kwargs)
