# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class NameModel (models.Model):
    """
        Abstract model representing 'name' field with apropriate unicode
        representation
    """
    name = models.CharField(u'название', max_length=255)

    __unicode__ = lambda self: self.name

    class Meta:
        abstract = True


class TimestampModel (models.Model):
    """
        Model representing creation and updatetin timestamp fields
    """

    created_at = models.DateTimeField(_('created at'), default=datetime.utcnow)
    updated_at = models.DateTimeField(_('updated at'), default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(TimestampModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class TaggableModel (models.Model):

    tags = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


    def __prepare_tags(self):
        if tags and len(tags):
            return ",".join([ tag.strip() for tag in self.tags.split(',')])

        else:
            return self.tags

    def save(self, *args, **kwargs):
        self.tags = self.__prepare_tags()
        super(TaggableModel, self).save(*args, **kwargs)


class SortableModel (models.Model):
    sort_order = models.IntegerField(_('sort order'), default=100)

    class Meta:
        abstract = True
        ordering = ["sort_order",]

