from django.db import models
from django.conf import settings
from django.utils import timezone

class Act(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    executer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='acts_executer')
    # user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    adress = models.CharField(max_length=200)
    act_type = models.CharField(max_length=20)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/act_images')
    file = models.FileField(null=True, blank=True, upload_to='files/act_files')
    completed = models.BooleanField(default=False)

    class ActProcesses(models.TextChoices):
        waiting = 'Ожидание принятия заявки'
        accepted = 'Заявки принята'
        returned = 'Заявка возвращена'

    act_processing = models.CharField(max_length=25, choices=ActProcesses.choices, default=ActProcesses.waiting)
    do_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['date_updated']
        # indexes = [models.Index(fields=['fieldname1', 'fieldname1']), ]

    def __str__(self):
        return self.title