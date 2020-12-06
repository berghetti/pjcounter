#!/usr/bin/env python3
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
import os
from pjcounter import analyzer

DIR_TESTE = './tests/'


dirs = os.listdir(DIR_TESTE)

for dir in dirs:
    print("Directory " + dir)
    dir += '/'
    files = os.listdir(DIR_TESTE + dir)

    for file in files:
        path_file = DIR_TESTE + dir + file

        try:
            job = analyzer.job(path_file)
            print("file \t %s"  %job.filename)
            print("pages \t%d"  %job.pages)
            print("copies \t%d" %job.copies)
            print("total \t%d"  %job.job_size)
            print()
        except:
            print("ERROR test file %s" %(path_file))
