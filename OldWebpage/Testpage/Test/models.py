from django.db import models

# Create your models here.
class PredictString(models.Model):
    text = models.CharField(max_length=25)

    def __str__(self):
        return self.text
