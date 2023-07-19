#!/usr/bin/python3
"""Defines fabric functions that distributes
an archive to web servers, deploys it, and cleans up after"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = [
    "54.157.187.24",
    "54.158.255.184"
]


def do_pack():
    """Generate an archive of /web_static folder"""
    try:
        os.makedirs("versions", exist_ok=True)
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        fn = "versions/web_static_{}.tgz".format(date)

        out = local("tar -czvf {} ./web_static/".format(fn))

        if out.succeeded:
            return "./{}".format(out.command.split(" ")[2])
        else:
            return None
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to web servers
    """
    archive_exists = os.path.exists(archive_path)
    if not archive_exists:
        return False

    try:
        archive_fn = archive_path.split("/")[-1]
        archive_dir = "/data/web_static/releases/{}".format(
            archive_fn.split(".")[0])

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(archive_dir))
        run("tar -xzf /tmp/{fn} --directory {dir}".format(
            fn=archive_fn, dir=archive_dir))
        run("rsync -a {dir}/web_static/* {dir}".format(dir=archive_dir))
        sudo("chown -R ubuntu:ubuntu /data/")
        run("rm -rf {dir}/web_static".format(dir=archive_dir))
        run("rm /tmp/{}".format(archive_fn))
        run("rm -rf /data/web_static/current")
        run("ln -sf {} /data/web_static/current".format(archive_dir))
        return True
    except Exception:
        return False


def do_clean(number=0):
    """Delete (total - number) amount of out-of-date archives
    """
    number = int(number)
    with lcd("./versions"):
        if number > 1:
            local("ls -t | tail -n +{} | xargs rm -f".format(number + 1))
        else:
            local("ls -t | tail -n +2 | xargs rm -f")
    with cd("/data/web_static/releases"):
        if number > 1:
            run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))
        else:
            run("ls -t | tail -n +2 | xargs rm -rf")


def deploy():
    """Archives and deploys the web_static folder"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
