import os
import hashlib


def hash_calc(project):
    module_dir = os.path.dirname(__file__)  # get current directory
    apk_path = os.path.join(module_dir, 'static/analyze/files/' + project.user_id + '/' + project.file)
    project.hash_md5 = md5(apk_path)
    project.hash_sha1 = sha1(apk_path)
    project.hash_sha256 = sha256(apk_path)
    project.hash_sha512 = sha512(apk_path)
    project.save()
    #project = models.Project()
    #project.file = apk_path


def md5(file_name):
    hash_value = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def sha1(file_name):
    hash_value = hashlib.sha1()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def sha256(file_name):
    hash_value = hashlib.sha256()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def sha512(file_name):
    hash_value = hashlib.sha512()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()

