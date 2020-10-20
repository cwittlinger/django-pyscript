from django.db import models
from djpyscript.fields import PyScriptField


class TestModel(models.Model):
    title = models.CharField(max_length=255)

    script = PyScriptField(injected_parameters=["number"], parameter_field="parameters")
    parameters = models.JSONField(default=dict, null=True, blank=True)

    script2 = PyScriptField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.parameters = self.script.extract_parameters()
        super().save(*args, **kwargs)
