#!/usr/bin/python3
"""
Fabric script (1-pack_web_static.py) that distributes an archive
To your web servers, using the function do_deploy
"""
from fabric.api import env, put, sudo, run


def do_deploy(archive_path):
    """Deploys the archive to web servers and updates the configuration."""
    if not local("test -f {}".format(archive_path)).succeeded:
        print("Archive not found: {}".format(archive_path))
        return False
    archive_name = os.path.basename(archive_path)

    for server in env.hosts:
        put(archive_path, f"/tmp/{archive_name}")
    for server in env.hosts:
        with sudo(server):
            run(f"tar -xvf /tmp/{archive_name} -C /data/web_static/releases")
            run(f"mv /data/web_static/releases/{archive_name[:-4]}
                    /data/web_static/releases/{archive_name}")
            run(f"rm /tmp/{archive_name}")
            run("rm -rf /data/web_static/current")
            run(f"ln -s /data/web_static/releases/{archive_name}
                    /data/web_static/current")
    for server in env.hosts:
        run("/path/to/restart_nginx.sh")
        return True
env.user = "ubuntu"
env.hosts = ["3.86.7.100", "100.26.212.112"]
archive_path = "/path/to/versions/web_static_20240403140823.tgz"
if do_deploy(archive_path):
    print("Deployment successful!")
else:
    print("Deployment failed!")
