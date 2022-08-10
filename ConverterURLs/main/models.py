from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy


class URL(models.Model):
    long_url = models.URLField(max_length=250)
    short_url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def __str__(self):
        return self.long_url

    def get_absolute_url(self):
        return reverse('reurl', kwargs={'url_pk': self.pk})
