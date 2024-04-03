#!/usr/bin/python3
"""Fabric script generates .tgz archive from contents of the web_static"""
from fabric.api import local, lcd
import time

def do_pack():
    """Generates a .tgz archive of the web_static folder and returns its path."""

    timestamp = time.strftime("%Y%m%d%H%M%S")  # Generate timestamp for archive name
    archive_path = f"versions/web_static_{timestamp}.tgz"

    try:
        with lcd("web_static"):
            local("mkdir -p ../versions")  # Create 'versions' directory if needed
            local(f"tar -cvzf ../{archive_path} .")  # Create the archive
            return archive_path
    except:
        return None
