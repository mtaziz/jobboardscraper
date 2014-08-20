from django.db import models
from django.core.urlresolvers import reverse

from organizations.models import Organization


class Job(models.Model):
    title = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    body = models.TextField()
    url = models.URLField('URL')
    pub_date = models.DateTimeField()
    scrape_date = models.DateTimeField()

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('jobs.views.job_detail', args=[str(self.pk)])
