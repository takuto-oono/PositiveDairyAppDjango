from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model


class DairyContent(models.Model):
    content = models.TextField(
        max_length=300, verbose_name='楽しかったことを記入しよう', null=True, blank=True)
    date = models.DateField(null=False, blank=True)
    ranking = models.IntegerField(null=False, blank=True)
    user_id = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="dairyContent")
    
