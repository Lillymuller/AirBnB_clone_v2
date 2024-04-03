#!/usr/bin/python3
"""
Fabric script (1-pack_web_static.py) that distributes an archive
To your web servers, using the function do_deploy
"""
from fabric.api import env, put, sudo, run
import os.path

env.hosts = ["3.86.7.100", "100.26.212.112"]


def do_deploy(archive_path):
    """
    Deploys the archive to web servers and updates the configuration
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}web_static".format(path_no_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_no_ext, symlink))
        return True
    except:
        return False
