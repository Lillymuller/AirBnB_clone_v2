#!/usr/bin/python3
"""Fabric to generates a .tgz archive from the contents of web_static"""
from fabric.api import local, run, prefix, env
from datetime import datetime
import os

env.hosts = ['localhost']


def do_pack():
    t = datetime.now()
    name = "web_static_{}{}{}{}{}{}.tgz".format(t.year, t.month,
                                                t.day, t.hour,
                                                t.minute, t.second)
    local('mkdir -p versions')
    local("tar -cvzf versions/{} web_static".format(name))
    size = os.stat("versions/{}".format(name)).st_size
    print("web_static packed: versions/{} -> {}".format(name, size))                              
