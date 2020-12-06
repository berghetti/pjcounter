#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import glob
import os
import shutil
try:
    from setuptools import setup
except ImportError as msg :
    sys.stderr.write("%s\n" % msg)
    sys.stderr.write(
    "You need the setuptools Python module.\n"
    "under Debian type 'sudo apt-get install python3-setuptools.'\n")
    sys.exit(1)


VERSION = "0.1"


setup(name = "pjcounter", # printer job counter
      version = VERSION,
      url = "http://www.pykota.com/software/pkpgcounter/",
      license = "GNU GPL",
      packages = [ "pjcounter" ])
