from django.contrib import admin

# Register your models here.
from .models import Project, Manifest, Avscan

admin.site.register(Project)
admin.site.register(Manifest)
admin.site.register(Avscan)
