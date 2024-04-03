#!/usr/bin/python3
"""Fabric script generates .tgz archive from contents of the web_static"""
import os
from datetime import datetime
from fabric.api import local


def create_archive():
    """Creates a tar gzipped archive of the directory web_static."""
    times = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(times.year,
                                                         times.month,
                                                         times.day,
                                                         times.hour,
                                                         times.minute,
                                                         times.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
        if local("tar -cvzf {} web_static".format(file)).failed is True:
            return None
        return file
