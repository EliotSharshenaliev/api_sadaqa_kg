from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )
