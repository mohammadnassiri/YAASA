import json
import datetime

from django.http import HttpResponse

from analyze.models import Project, User, Manifest, Avscan
import analyze.libs.threads as threads
import analyze.libs.hashes as hashes
from django.shortcuts import render

from apksa import settings
from .forms import CreateProject


def index(request):
    threads.project_thread_manager()
    return render(request, "analyze/index.html")


def create_project(request):
    message = ""
    message_type = ""
    if request.method == 'POST':
        form = CreateProject(request.POST, request.FILES)
        project = Project()
        user = User.objects.get(id=1)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.file = request.FILES['file']
            project.status = 0
            project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            project.save()
            path = settings.MEDIA_ROOT + project.file.name
            project.hash_md5 = hashes.md5(path)
            project.hash_sha1 = hashes.sha1(path)
            project.hash_sha256 = hashes.sha256(path)
            project.hash_sha512 = hashes.sha512(path)
            project.save()
            if project.id:
                message = "Scan has been submitted."
                message_type = "success"
            else:
                message = "There is a problem. Please try again later."
                message_type = "danger"

            threads.project_thread_create(project)
    else:
        form = CreateProject()
    projects = Project.objects.order_by('-id')
    for p in projects:
        if p.status == 0:
            p.status = "Pending"
        elif p.status == 1:
            p.status = "Unzipping"
        elif p.status == 2:
            p.status = "Scanning"
        elif p.status == 3:
            p.status = "AV Scanning"
        elif p.status == 4:
            p.status = True
        else:
            p.status = "Please contact support."
    return render(request, 'analyze/create_project.html',
                  {'form': form, 'message': message, 'message_type': message_type,
                   'projects': projects})


def report_project(request, project_id):
    project_cleans = 0
    project_warnings = 0
    project_dangers = 0
    project = Project.objects.get(pk=project_id)

    manifest = Manifest.objects.order_by('-id').filter(project_id=project_id).first()
    manifest.uses_permission = json.loads(manifest.uses_permission.replace("'", '"'))
    manifest.activities = json.loads(manifest.activities.replace("'", '"'))
    manifest.libraries = json.loads(manifest.libraries.replace("'", '"'))
    manifest.providers = json.loads(manifest.providers.replace("'", '"'))
    manifest.receivers = json.loads(manifest.receivers.replace("'", '"'))
    manifest.services = json.loads(manifest.services.replace("'", '"'))

    avscan = Avscan.objects.order_by('-id').filter(project_id=project_id).first()

    avscan.clamav_engine = "Not Ready"
    avscan.clamav_engine_version = ""
    avscan.clamav_pest_name = ""

    #avscan.bitdefender = json.loads(avscan.bitdefender)
    #avscan.bitdefender_engine = avscan.bitdefender[0]['engine']
    #avscan.bitdefender_engine_version = avscan.bitdefender[0]['engine_version']
    #avscan.bitdefender_pest_name = avscan.bitdefender[0]['pest_name'] if avscan.bitdefender[0]['pest_name'] else "Clean"
    #if avscan.bitdefender[0]['pest_name']:
    #    project_dangers += 1
    #else:
    #    project_cleans += 1

    avscan.bitdefender_engine = "Not Ready"
    avscan.bitdefender_engine_version = ""
    avscan.bitdefender_pest_name = ""

    avscan.esetnod32_engine = "Not Ready"
    avscan.esetnod32_engine_version = ""
    avscan.esetnod32_pest_name = ""

    return render(request, 'analyze/report_project.html',
                  dict(manifest=manifest, project_name=project.name, avscan=avscan, project_cleans=project_cleans,
                       project_dangers=project_dangers))
