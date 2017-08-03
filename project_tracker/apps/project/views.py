# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from .models import ProjectGroup
from .models import Project

from .forms import ProjectGroupSearchForm, ProjectSearchForm

import csv, time


class ProjectGroupListView(ListView):

    model = ProjectGroup
    slug_field = "short"
    template_name = "projectgroup_list.html"
    context_object_name = "project_group_list"
    form_class = ProjectGroupSearchForm

o    def get_queryset(self):
        form = self.form_class(self.request.GET)
        qs = super(ProjectGroupListView, self).get_queryset()
        if form.is_valid():
            return qs.filter(
                Q(short__icontains=form.cleaned_data["search"]) |
                Q(name__icontains=form.cleaned_data["search"])
            )
        return qs

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
    form_class = ProjectGroupSearchForm

    def get_context_data(self, **kwargs):
        context = super(ProjectGroupDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        form = self.form_class(self.request.GET)
        projects = obj.project_set.all()
        if form.is_valid():
            projects = projects.filter(
                Q(short__icontains=form.cleaned_data["search"]) |
                Q(name__icontains=form.cleaned_data["search"]) |
                Q(description__icontains=form.cleaned_data["search"])
            )
        context["projects"] = projects
        return context

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
    form_class = ProjectSearchForm

    def render_to_response(self, context, **response_kwargs):
        """
        Creates a CSV response if requested, otherwise returns the default
        template response.
        """
        # Sniff if we need to return a CSV export
        if self.request.GET.get('format', '') == 'csv':
            response = HttpResponse(content_type='text/csv')
            group = self.get_object()
            print(type(group))
            response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"' % (group.short, time.strftime("%Y-%m-%d"))
            projects = group.project_set.all()
            writer = csv.writer(response)
            writer.writerow(['short', 'name', 'owner', 'description', 'is closed'])
            for item in projects:
                writer.writerow([item.short, item.name, item.owner, item.description, item.is_closed])
            return response
        else:
            return super(ProjectDetailView, self).render_to_response(context, **response_kwargs)


def main(request):
    return render(request, 'main.html')
