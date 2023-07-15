#!/usr/bin/python3
"""Defines a function do_pack() which generates a .tgz archive
from the contents of the web_static folder"""

from fabric.api import *


def do_pack():
    """Generate an archive of /web_static folder"""

    local("mkdir versions -p")
    date = local("date '+%Y%m%d%H%M%s'", capture=True)
    local("tar -czvf versions/web_static_{}.tgz web_static".format(date))
