import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


class Deployer:
    def __init__(self, hosts):
        self.hosts = hosts

    def create_archive(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"

        try:
            print("Packing web_static to {}".format(archive_path))
            local(f"tar -cvzf {archive_path} web_static")
            archive_size = os.stat(archive_path).st_size
            print(f"web_static packed: {archive_path} -> {archive_size} Bytes")
        except Exception as e:
            print(f"Error creating archive: {e}")
            archive_path = None

        return archive_path

    @runs_once
    def deploy_archive(self, archive_path):
        if not os.path.exists(archive_path):
            return False

        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace(".tgz", "")
        folder_path = f"/data/web_static/releases/{folder_name}/"

        try:
            put(archive_path, f"/tmp/{file_name}")
            run(f"mkdir -p {folder_path}")
            run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
            run(f"rm -rf /tmp/{file_name}")
            run(f"mv {folder_path}web_static/* {folder_path}")
            run(f"rm -rf {folder_path}web_static")
            run(f"rm -rf /data/web_static/current")
            run(f"ln -s {folder_path} /data/web_static/current")
            print("New version deployed!")
            return True
        except Exception as e:
            print(f"Error during deployment: {e}")
            return False


if __name__ == "__main__":
    deployer = Deployer(hosts=['3.86.7.100', '100.26.212.112'])
    archive_path = deployer.create_archive()
    if archive_path:
        deployer.deploy_archive(archive_path)
