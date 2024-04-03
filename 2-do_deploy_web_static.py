#!/usr/bin/python3
'''fabfile tar packaging'''
from fabric.api import local, run, env, put
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['3.86.7.100', '100.26.212.112']


def do_pack():
    """Packes web_static in tgz format"""
    t = datetime.now()
    name = "web_static_{}{}{}{}{}{}.tgz".format(t.year, t.month,
                                                t.day, t.hour,
                                                t.minute, t.second)
    local('mkdir -p versions')
    local("tar -cvzf versions/{} web_static".format(name))
    size = os.stat("versions/{}".format(name)).st_size
    print("web_static packed: versions/{} -> {}".format(name, size))


def do_deploy(archive_path):
    if not archive_path:
        return(False)
    name = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(name, name))
        run("rm /tmp/{}".format(name))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed")
        return(True)
    except BaseException:
        return(False)
