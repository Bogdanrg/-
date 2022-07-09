from django.db import models
from django.contrib.auth.models import User


class HistoryURLs(models.Model):
    url = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
