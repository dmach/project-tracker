# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import json

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince

from ..project import models as project_models


class Dashboard(models.Model):
    owner               = models.ForeignKey(settings.AUTH_USER_MODEL)

    # link to projects
    projects            = models.ManyToManyField(project_models.Project, blank=True)

    source_class        = models.CharField(max_length=100, blank=False)
    name                = models.CharField(max_length=30, db_index=True)
    description         = models.CharField(max_length=200, blank=True)

    nobody              = models.CharField(max_length=1000, blank=True)
    aliases             = models.TextField(max_length=10000, blank=True)

    # url & auth
    # * TODO: github - generate a token via web browser
    url                 = models.CharField(max_length=200)
    username            = models.CharField(max_length=100, blank=True, null=True)
    password            = models.CharField(max_length=100, blank=True, null=True)
    token               = models.CharField(max_length=200, blank=True, null=True)

    # query
    query_query         = models.CharField(max_length=1000, blank=True, null=True)
    query_project       = models.CharField(max_length=200, blank=True, null=True)
    query_users         = models.CharField(max_length=200, blank=True, null=True)

    # colors
    age_days_blue       = models.PositiveIntegerField(blank=True, null=True)
    age_days_yellow     = models.PositiveIntegerField(blank=True, null=True)
    age_days_red        = models.PositiveIntegerField(blank=True, null=True)

    # dates - dashboard configuration
    date_created        = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated        = models.DateTimeField(auto_now=True, db_index=True)
    date_closed         = models.DateTimeField(blank=True, null=True, db_index=True)

    # dates - dashboard contents
    date_synced         = models.DateTimeField(blank=True, null=True, db_index=True)

    def add_to_project(self, project):
        self.projects.add(project)

    @property
    def issues(self):
        return self.issue_set.filter(parent__isnull=True)

    @property
    def count_all_issues(self):
        return self.issue_set.count()

    @property
    def count_open_issues(self):
        return self.issue_set.filter(is_closed=False).count()


class Tag(models.Model):
    name                = models.CharField(max_length=100)
    color               = models.CharField(max_length=100, blank=True, null=True)


class Issue(models.Model):
    dashboard           = models.ForeignKey(Dashboard)
    parent              = models.ForeignKey("self", blank=True, null=True, related_name="children")
    children_count      = models.PositiveIntegerField(default=0)

    # identity
    issue_type          = models.CharField(max_length=20)
    issue_id            = models.PositiveIntegerField(blank=True, null=True)
    # internal id within a project (pull request ID, taiga issue ID in a board, ...)
    issue_ref           = models.PositiveIntegerField(blank=True, null=True)
    summary             = models.CharField(max_length=200)
    url                 = models.URLField(max_length=500, blank=True, null=True)

    # project
    project             = models.CharField(max_length=200, blank=True, null=True)
    component           = models.CharField(max_length=200, blank=True, null=True)

    # status
    status              = models.CharField(max_length=50, db_index=True)
    is_closed           = models.BooleanField(default=False, db_index=True)
    is_blocked          = models.BooleanField(default=False, db_index=True)

    # people
    # TODO: devel, qe, docs owner
    # TODO: normalized fields for stats (apply username substitutions)
    assignee            = models.CharField(max_length=100, blank=True, db_index=True)
    reporter            = models.CharField(max_length=100, blank=True, db_index=True)

    # priorities
    priority            = models.CharField(max_length=20)
    severity            = models.CharField(max_length=20)

    # dates
    date_created        = models.DateTimeField(blank=True, null=True, db_index=True)
    date_updated        = models.DateTimeField(blank=True, null=True, db_index=True)
    date_closed         = models.DateTimeField(blank=True, null=True, db_index=True)
    date_due            = models.DateTimeField(blank=True, null=True, db_index=True)

    # tags
    # TODO: consider replacing with ManyToManyField if pgsql performs well
    tags                = models.TextField(max_length=4000, blank=True, null=True)

    class Meta:
        unique_together = (
            ("dashboard", "issue_id"),
        )
        ordering = ("-date_created", "date_closed")

    def __unicode__(self):
        return u"%s: %s - %s" % (self.dashboard.name, self.issue_id, self.summary)

    def save(self, *args, **kwargs):
        if self.parent:
            self.parent.children_count = self.parent.children.all().count()
            self.parent.save()
        self.children_count = self.children.all().count()
        super(Issue, self).save(*args, **kwargs)

    def _date(self, d):
        if d in (None, ""):
            return ""
        return d.strftime("%Y-%m-%d")

    def get_date_created_display(self):
        return self._date(self.date_created)

    def get_date_updated_display(self):
        return self._date(self.date_updated)

    def get_date_closed_display(self):
        return self._date(self.date_closed)

    def get_date_due_display(self):
        return self._date(self.date_due)

    def timesince_created(self):
        return timesince(self.date_created)

    def tags_dict(self):
        if not self.tags:
            return {}
        return json.loads(self.tags)

    def set_tags(self, tag_color_dict):
        if isinstance(tag_color_dict, list):
            tag_color_dict = {i: None for i in tag_color_dict}
        self.tags = json.dumps(tag_color_dict)
