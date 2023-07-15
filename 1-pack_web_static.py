#!/usr/bin/python3
"""Defines a function do_pack() which generates a .tgz archive
from the contents of the web_static folder"""

from fabric.api import *
from datetime import datetime
import os


def do_pack():
    """Generate an archive of /web_static folder"""

    d = datetime.now()
    date = d.strftime('%Y%m%d%H%M%S')
    os.makedirs("versions", exist_ok=True)

    out = local("tar -czvf versions/web_static_{}.tgz web_static".format(date),
                capture=True)

    if out.succeeded:
        return "./{}".format(out.command.split(" ")[2])
    else:
        return None
