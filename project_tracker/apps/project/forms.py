# -*- coding: utf-8 -*-

from django import forms


class ProjectGroupSearchForm(forms.Form):
    search = forms.CharField()


class ProjectSearchForm(forms.Form):
    search = forms.CharField()
