#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean
"""
from fabric.api import env, local, run, sudo
import os

env.hosts = ["3.86.7.100", "100.26.212.112"]


def do_clean(number=0):
    """Deletes out-of-date archives on local and remote servers
    Args:
    number (int): The number of archives to keep
    (default: 0, keeps only the most recent)

    Raises:
    ValueError: If the provided number is negative
    """

    if number < 0:
        raise ValueError("Number of archives to keep cannot be negative")

    """Delete local archives"""
    local_archives = sorted(local("ls versions/").split())[::-1]
    for archive in local_archives[number:]:
        local("rm versions/{}".format(archive))

"""Delete remote archives (assuming sudo access)"""
for server in env.hosts:
    with sudo(server):
    remote_archives = run("ls -tr /data/web_static/releases/ | grep
            'web_static_'").split()
    remote_archives = remote_archives[::-1][:number]

    for archive in set(remote_archives):
        run("rm -rf /data/web_static/releases/{}".format(archive))
