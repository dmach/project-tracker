# -*- coding: utf-8 -*-

from django import forms
from .models import ProjectGroup, Project, ProjectPhase
from django.db.models import Q


class ProjectGroupSearchForm(forms.Form):
    search = forms.CharField()

    def get_query(self, projects):
        self.is_valid()
        search = self.cleaned_data["search"]

        query = Q()

        if search:
            query = projects.filter(
                Q(short__icontains=search) |
                Q(name__icontains=search)
            )
        return query


class ProjectSearchForm(forms.Form):
    search = forms.CharField()

    def get_query(self, projects):
        self.is_valid()
        search = self.cleaned_data["search"]

        query = Q()

        if search:
            query = projects.filter(
                Q(short__icontains=search) |
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return query


class ProjectPhaseSearchForm(forms.Form):
    search = forms.CharField()

    def get_query(self, projects):
        self.is_valid()
        search = self.cleaned_data["search"]

        query = Q()

        if search:
            query = projects.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return query