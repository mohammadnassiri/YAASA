import os
import datetime
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    hash_md5 = models.TextField()
    hash_sha1 = models.TextField()
    hash_sha256 = models.TextField()
    hash_sha512 = models.TextField()
    time = models.CharField(max_length=255)
    status = models.IntegerField()


class Manifest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    activities = models.TextField()
    libraries = models.TextField()
    min_sdk = models.TextField()
    providers = models.TextField()
    receivers = models.TextField()
    services = models.TextField()
    target_sdk = models.TextField()
    uses_permission = models.TextField()
    version_code = models.TextField()
    version_name = models.TextField()


class Avscan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    clamav = models.TextField()
    bitdefender = models.TextField()
    esetnod32 = models.TextField()
