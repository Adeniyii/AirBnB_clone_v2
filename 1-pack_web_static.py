#!/usr/bin/python3
"""Defines a function do_pack() which generates a .tgz archive
from the contents of the web_static folder"""

from fabric.api import *
from datetime import datetime
import os


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
