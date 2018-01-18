import os
import datetime
import subprocess
import zipfile
import axmlparserpy as ApkParser
from analyze.models import Project, Manifest, Avscan
from threading import Thread
from subprocess import Popen


def get_full_path(path):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(module_dir, path)
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
    #avscan_tool(project)


def unzip_tool(project):
    project.status = 1
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
    path = get_full_path(project.file.name)
    zip_ref = zipfile.ZipFile(path.replace('/', '\\'), 'r')
    save_path = path.rsplit(".", 1)[0].replace('/', '\\') + "-unzipped"
    zip_ref.extractall(save_path)
    zip_ref.close()


def apk_tool(project):
    project.status = 2
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
    path = get_full_path(project.file.name)
    apk_path = path.replace('/', '\\')
    save_path = path.rsplit(".", 1)[0].replace('/', '\\')
    tool_path = get_full_path('tools\\apktool\\apktool.jar')
    cmd = "java -jar " + tool_path + " d " + apk_path + " -o " + save_path + " -f"
    p = Popen(cmd)
    p.communicate()
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()


def parse_manifest(project):
    manifest = Manifest()
    manifest.project = project
    path = get_full_path(project.file.name)
    manifest_path = path.replace('/', '\\')
    parsed_apk = ApkParser.APK(manifest_path)
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
    path = get_full_path(project.file.name)
    apk_path = path.replace('/', '\\')
    tool_path = get_full_path('tools\\plagueScanner\\plaguescanner.py')
    proc = subprocess.Popen(['python', tool_path,  apk_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0]
    avscan = Avscan()
    avscan.project = project
    avscan.clamav = ""
    avscan.bitdefender = output
    avscan.esetnod32 = ""
    avscan.save()
    project.status = 4
    project.time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    project.save()
