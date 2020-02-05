from django.db import models

# Create your models here.
class E_mail(models.Model):
    text = models.CharField(max_length=1024)
    time_to_send = models.IntegerField()
    sent = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
