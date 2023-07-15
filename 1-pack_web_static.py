#!/usr/bin/python3
"""Defines a function do_pack() which generates a .tgz archive
from the contents of the web_static folder"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """Generate an archive of /web_static folder"""

    d = datetime.now()
    date = d.strftime('%Y%m%d%H%M%S')

    local("mkdir versions -p")
    local("tar -czvf versions/web_static_{}.tgz web_static".format(date))
