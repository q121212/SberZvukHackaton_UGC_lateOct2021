from django.db import models


class Recognize(models.Model):
    source = models.URLField(null=False)
    prefix = models.CharField(max_length=128, null=False)

    def __str__(self):
        return f'{self.source}, {self.prefix}'
