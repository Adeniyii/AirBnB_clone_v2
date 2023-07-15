#!/usr/bin/env python3
"""Fabric script that defines a function do_pack()
which generates a .tgz archive from the contents of the
web_static folder, using the function"""

from fabric.api import *


def do_pack():
    local("mkdir versions -p")
    date = local("date '+%Y%m%d%H%M%s'", capture=True)
    cmd_output = local(
        "tar -czvf versions/web_static_{date}.tgz web_static".format(
            date=date), capture=True)

    if cmd_output.failed:
        return None
    else:
        return local("echo {} | cut -d ' ' -f3".format(
            cmd_output.command), capture=True)
