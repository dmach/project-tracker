# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


PROJECT_STATUS_COLOR_ENUM = (
    (0, "green"),
    (1, "yellow"),
    (2, "red"),
)


@python_2_unicode_compatible
class ProjectGroup(models.Model):
    short               = models.CharField(max_length=20, unique=True)
    name                = models.CharField(max_length=100, db_index=True)
    owner               = models.ForeignKey(settings.AUTH_USER_MODEL)

    date_created        = models.DateTimeField(auto_now_add=True, db_index=True)
    date_closed         = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.short


@python_2_unicode_compatible
class Project(models.Model):
    group               = models.ForeignKey(ProjectGroup)
    short               = models.CharField(max_length=20, db_index=True)
    name                = models.CharField(max_length=100, db_index=True)
    description         = models.CharField(max_length=200, blank=True)
    owner               = models.ForeignKey(settings.AUTH_USER_MODEL)
    members             = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="project_members")

    date_created        = models.DateTimeField(auto_now_add=True, db_index=True)
    date_closed         = models.DateTimeField(null=True, blank=True, db_index=True)

    # automatically set according to date_closed in save()
    is_closed           = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = (
            ("group", "short"),
        )
        ordering = ("is_closed", "short")

    def __str__(self):
        return "{}/{}".format(self.group, self.short)

    def save(self, *args, **kwargs):
        if self.date_closed:
            self.is_closed = True
        else:
            self.is_closed = False
        return super(Project, self).save(*args, **kwargs)

    def add_member(self, user):
        self.members.add(user)


@python_2_unicode_compatible
class ProjectPhase(models.Model):
    project             = models.ForeignKey(Project)
    name                = models.CharField(max_length=50)
    description         = models.CharField(max_length=200, blank=True)
    status_color        = models.IntegerField(null=True, choices=PROJECT_STATUS_COLOR_ENUM)
    completed           = models.IntegerField(null=True)

    date_due            = models.DateTimeField()
    date_due_planned    = models.DateTimeField()

    def __str__(self):
        return self.name
