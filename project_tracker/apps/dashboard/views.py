# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.views.generic import DetailView

from .models import Dashboard


class DashboardDetailView(DetailView):

    model = Dashboard
    slug_field = "name"
    template_name = "dashboard_detail.html"
    context_object_name = "dashboard"

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        issues = obj.issue_set.filter(parent__isnull=True)
        if self.kwargs.get("state", None) == "open":
            issues = obj.issue_set.filter(parent__isnull=True, is_closed=False)
        context["issues"] = issues
        return context
