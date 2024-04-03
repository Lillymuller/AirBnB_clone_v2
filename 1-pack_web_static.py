#!/usr/bin/python3
"""Fabric script generates .tgz archive from contents of the web_static"""
import os
from datetime import datetime
from fabric.api import local


def create_archive():
    """Creates a tar gzipped archive of the directory web_static."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    os.makedirs("versions", exist_ok=True)
    if local(f"tar -cvzf {archive_path} web_static").failed:
        return None 
    return archive_path
