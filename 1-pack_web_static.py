#!/usr/bin/python3
"""Fabric script generates .tgz archive from contents of the web_static"""
from fabric.api import local, lcd
import time


def do_pack():
    """Generates a .tgz archive of the web_static folder and returns path"""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"
    try:
        with lcd("web_static"):
            local("mkdir -p ../versions")
            local(f"tar -cvzf ../{archive_path} .")
            return archive_path
    except:
        return None
