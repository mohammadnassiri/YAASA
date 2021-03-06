import os
import datetime
import subprocess
import zipfile

from analyze.models import Project, Manifest, Avscan
from threading import Thread
import tools.axmlparserpy.apk as ApkParser

from apksa import settings


def get_file_path(path):
    directory = os.path.join(settings.MEDIA_ROOT, path)
    return directory


def get_tool_path(path):
    directory = os.path.join(settings.TOOLS_DIR, path)
    return directory


def project_thread_manager():
    project = Project.objects.order_by('-id').filter(status=1).first()
    if project is not None and (
                datetime.datetime.strptime(project.time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(hours=1)) \
            < datetime.datetime.now():
        project_thread_create(project)
    if project is None:
        project = Project.objects.order_by('-id').filter(status=0).first()
        if project is not None:
            project_thread_create(project)


def project_thread_create(project):
    t = Thread(target=do_tools, args=(project,))
    t.start()


def do_tools(project):
    unzip_tool(project)
    apk_tool(project)
    parse_manifest(project)
    avscan_tool(project)


def unzip_tool(project):
    project.status = 1
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
    path = get_file_path(project.file.name)
    zip_ref = zipfile.ZipFile(path, 'r')
    save_path = path.rsplit(".", 1)[0] + "-unzipped"
    zip_ref.extractall(save_path)
    zip_ref.close()


def apk_tool(project):
    project.status = 2
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
    path = get_file_path(project.file.name)
    save_path = path.rsplit(".", 1)[0]
    tool_path = get_tool_path('apktool/apktool.jar')
    subprocess.Popen(['java', '-jar', tool_path, 'd', path, '-o', save_path, '-f'], stdout=subprocess.PIPE)
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()


def parse_manifest(project):
    manifest = Manifest()
    manifest.project = project
    path = get_file_path(project.file.name)
    parsed_apk = ApkParser.APK(path)
    manifest.activities = parsed_apk.get_activities()
    manifest.receivers = parsed_apk.get_receivers()
    manifest.services = parsed_apk.get_services()
    manifest.uses_permission = parsed_apk.get_permissions()
    manifest.version_code = parsed_apk.get_androidversion_code()
    manifest.version_name = parsed_apk.get_androidversion_name()
    manifest.libraries = parsed_apk.get_libraries()
    manifest.providers = parsed_apk.get_providers()
    manifest.min_sdk = parsed_apk.get_min_sdk_version()
    manifest.target_sdk = parsed_apk.get_target_sdk_version()
    manifest.save()


def avscan_tool(project):
    project.status = 3
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
    path = get_file_path(project.file.name)
    tool_path = get_tool_path('plagueScanner/plaguescanner.py')
    proc = subprocess.Popen(['python3', tool_path, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0].strip().decode('utf-8')
    avscan = Avscan()
    avscan.project = project
    avscan.clamav = ""
    avscan.bitdefender = output
    avscan.esetnod32 = ""
    avscan.save()
    project.status = 4
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
