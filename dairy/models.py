from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from members.models import Group
import uuid

class Event(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)

    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='EventCreator', blank=True, null=True)
    creationTime = models.DateTimeField(null=True, blank=True)
    lastEditor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='EventLastEditor', blank=True, null=True)
    lastEditTime = models.DateTimeField(null=True, blank=True)
    admins = models.ManyToManyField(User, related_name='EventAdmins', blank=True)
    sharedGroups = models.ManyToManyField(Group, blank=True)
    isPublic = models.BooleanField(default=True)

    startTimestamp = models.DateField(verbose_name="Start Time")
    endTimestamp = models.DateField(verbose_name="End Time", null=True, blank=True)
    isAllDay = models.BooleanField(default=False)
    details = RichTextField(max_length=5000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.name



class Certificate(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4,unique=True)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Name of the Participant')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)
    issue_date = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = "Certificate"

    def __str__(self):
        return self.name
