# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin


class FormPlugin(CMSPlugin):

    name = models.CharField(_('Name'), max_length=50, help_text=_('Used to filter out form submissions.'))

    def __unicode__(self):
        return self.name


class FieldsetPlugin(CMSPlugin):

    legend = models.CharField(_('Legend'), max_length=50, blank=True)

    def __unicode__(self):
        return self.legend or str(self.pk)


class FieldPlugin(CMSPlugin):
    """
    A general field model.

    The reason it's flat instead of having a nice structure is, as we read in
    CMSPlugin docs:

    > 1. subclasses of CMSPlugin *cannot be further subclassed*
    """

    label = models.CharField(_('Label'), max_length=50)
    required = models.BooleanField(_('Field is required'), default=True)
    placeholder_text = models.CharField(_('Placeholder text'), max_length=50)
    help_text = models.TextField(_('Help text'), blank=True, null=True,
                                 help_text=_('Explanatory text displayed next to input field. Just like this one.'))

    # for text field those are min and max length
    # for multiple select those are min and max number of choices
    min_value = models.PositiveIntegerField(_('Min value'), blank=True, null=True)
    max_value = models.PositiveIntegerField(_('Max value'), blank=True, null=True)

    def copy_relations(self, oldinstance):
        for option in oldinstance.option_set.all():
            option.pk = None  # copy on save
            option.field = self
            option.save()

    def __unicode__(self):
        return self.label


class Option(models.Model):

    value = models.CharField(_('Value'), max_length=50)
    field = models.ForeignKey(FieldPlugin, editable=False)

    def __unicode__(self):
        return self.value


class ButtonPlugin(CMSPlugin):

    label = models.CharField(_('Label'), max_length=50)

    def __unicode__(self):
        return self.label