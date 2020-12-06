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

"""This is the main module of pjcounter

It defines the PDLAnalyzer class, which provides a generic way to parse
input files, by automatically detecting the best parser to use."""

import sys
import os
import tempfile
import logging
import warnings

from . import pdlparser, postscript, pdf, pcl345, pclxl

class PDLAnalyzer:
    """Class for PDL autodetection."""
    def __init__(self, filename):
        """Initializes the PDL analyzer.

           filename is the name of the file or '-' for stdin.
           filename can also be a file-like object which
           supports read() and seek().
        """
        self.filename = filename
        self._workfile = None

        self._parser = None


    def _detectPDLHandler(self):
        """Tries to autodetect the document format.

           Returns the correct PDL handler class or None if format is unknown
        """

        if self._parser:
            return

        if not os.stat(self.filename).st_size:
            raise pdlparser.PDLParserError("input file %s is empty !" % str(self.filename))
        (firstblock, lastblock) = self._readFirstAndLastBlocks(self._workfile)
        # IMPORTANT: the order is important below. FIXME.
        for module in (postscript, \
                       pclxl, \
                       pdf, \
                       pcl345):
            try:
                self._parser = module.Parser(self, self.filename,
                                           (firstblock, lastblock))
                break
            except pdlparser.PDLParserError:
                pass # try next parser

        if not self._parser:
            raise pdlparser.PDLParserError("Analysis of first data block failed.")

    @property
    def _pdlhandler(self):
        if not self._parser:
            self._detectPDLHandler()
        return self._parser


    def _openFile(self):
        """Opens the job's data stream for reading."""
        if hasattr(self.filename, "read") and hasattr(self.filename, "seek"):
            # filename is in fact a file-like object
            infile = self.filename
        elif self.filename == "-":
            # we must read from stdin
            infile = sys.stdin
        else:
            # normal file
            self._workfile = open(self.filename, "rb")
            return

        # Use a temporary file, always seekable contrary to standard input.
        self._workfile = tempfile.NamedTemporaryFile(mode="w+b",
                                                    prefix="pjcounter_",
                                                    suffix=".prn",
                                                    dir=os.environ.get("PYKOTADIRECTORY") or tempfile.gettempdir())
        self.filename = self._workfile.name
        while True:
            data = infile.read(pdlparser.MEGABYTE)
            if not data:
                break
            self._workfile.write(data)
        self._workfile.flush()
        self._workfile.seek(0)

    def _closeFile(self):
        """Closes the job's data stream if we have to."""
        self._workfile.close()

    def _readFirstAndLastBlocks(self, inputfile):
        """Reads the first and last blocks of data."""
        # Now read first and last block of the input file
        # to be able to detect the real file format and the parser to use.
        firstblock = inputfile.read(pdlparser.FIRSTBLOCKSIZE)
        try:
            inputfile.seek(-pdlparser.LASTBLOCKSIZE, 2)
            lastblock = inputfile.read(pdlparser.LASTBLOCKSIZE)
        except IOError:
            lastblock = ""
        return (firstblock, lastblock)


    def _getJobSize(self):
        """Returns the job's size."""
        pages = 0
        copies = 0
        self._openFile()
        try:
            try:
                pages, copies = self._pdlhandler.getJobSize()
            except pdlparser.PDLParserError as msg:
                raise pdlparser.PDLParserError("Unsupported file format for %s (%s)" % (self.filename, msg))
        finally:
            self._closeFile()

        return pages, copies


class job(PDLAnalyzer):
    def __init__(self, filename):
        super().__init__(filename)
        self.pages, self.copies = self._getJobSize()
        self.job_size = self.pages * self.copies
