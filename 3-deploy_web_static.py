#!/usr/bin/python3
"""Creates a .tgz archive of the web_static folder with a timestamped name."""
import os
from fabric.api import env, local, put, run, sudo

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_pack():
    """Creates a .tgz archive of the web_static folder with a timestamped name."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    try:
        local("mkdir -p versions")
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Deploys the archive to web servers and updates the configuration."""
    if not os.path.isfile(archive_path):
        print("Archive not found:", archive_path)
        return False
    archive_name = os.path.basename(archive_name)

    for server in env.hosts:
        try:
            put(archive_path, f"/tmp/{archive_name}")
            with sudo(server):
                run(f"tar -xzf /tmp/{archive_name} -C /data/web_static/releases")
                run(f"mv /data/web_static/releases/{archive_name[:-4]} /data/web_static/releases/{archive_name}")
                run(f"rm /tmp/{archive_name}")
                run("rm -rf /data/web_static/current")
                run(f"ln -s /data/web_static/releases/{archive_name} /data/web_static/current")
                run("/path/to/restart_nginx.sh")
        except:
            return False
    return True

def deploy():
    """Creates and deploys an archive to web servers."""
    archive_path = do_pack()

    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
