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

"""This modules implements a page counter for PDF documents.

   Some informations taken from PDF Reference v1.7 by Adobe.
"""

import re

from . import pdlparser

PDFWHITESPACE = chr(0) \
                + chr(9) \
                + chr(10) \
                + chr(12) \
                + chr(13) \
                + chr(32)
PDFDELIMITERS = r"()<>[]{}/%"
PDFMEDIASIZE = "/MediaBox [xmin ymin xmax ymax]" # an example. MUST be present in Page objects

class Parser(pdlparser.PDLParser):
    """A parser for PDF documents."""
    totiffcommands = [ 'gs -sDEVICE=tiff24nc -dPARANOIDSAFER -dNOPAUSE -dBATCH -dQUIET -r"%(dpi)i" -sOutputFile="%(outfname)s" "%(infname)s"' ]
    required = [ "gs" ]
    openmode = "rb"
    format = "PDF"
    def isValid(self):
        """Returns True if data is PDF, else False."""
        if self.firstblock.startswith(b"%PDF-") or \
           self.firstblock.startswith(b"\033%-12345X%PDF-") or \
           ((self.firstblock[:128].find(b"\033%-12345X") != -1) and (self.firstblock.upper().find(b"LANGUAGE=PDF") != -1)) or \
           (self.firstblock.find(b"%PDF-") != -1):
            return True
        else:
            return False

    def getJobSize(self):
        """Counts pages in a PDF document.

           This method works great in the general case,
           and is around 30 times faster than the active
           one.
           Unfortunately it doesn't take into account documents
           with redacted pages (only made with FrameMaker ?)
           where an existing PDF object is replaced with one
           with the same major number a higher minor number.
        """
        newpageregexp = re.compile(r"/Type\s*/Page[/>\s]")

        pages = len(newpageregexp.findall(self.infile.read().decode('utf-8', 'replace')))

        if pages:
            return pages, 1
        else:
            return None, None
