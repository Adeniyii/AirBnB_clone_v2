#!/usr/bin/python3
"""Defines a fabric function `do_deploy` that distributes
an archive to web servers"""

from fabric.api import *
import os

env.hosts = [
    "54.157.187.24",
    "54.158.255.184"
]

env.user = "ubuntu"


def do_deploy(archive_path):
    """distributes an archive to web servers
    """
    try:
        archive_exists = os.path.exists(archive_path)
        if not archive_exists:
            return False

        archive_fn = archive_path.split("/")[-1]
        archive_dir = "/data/web_static/releases/{}".format(
            archive_fn.split(".")[0])

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(archive_dir))
        run("tar -xzf /tmp/{fn} --directory {dir}".format(
            fn=archive_fn, dir=archive_dir))
        run("mv {dir}/web_static/* {dir}".format(dir=archive_dir))
        run("rm -rf {dir}/web_static")
        run("rm /tmp/{}".format(archive_fn))
        run("rm -rf /data/web_static/current")
        run("ln -sf {} /data/web_static/current".format(archive_dir))
    except Exception:
        return False
