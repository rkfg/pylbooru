#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
#
#    tagfilter V 1.2
#
#    (C) 27.06.2010 eurekafag <eurekafag@eureka7.ru>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# REQUIRES: GNU coreutils, Imagemagick, filesystem with hardlink support
#

import os, sys

try:
    import sqlite3
except:
    print "No sqlite python module found."
    sys.exit(1)

TAGSDIR = "~/pics"

conn = sqlite3.connect("pylbooru.db")
c = conn.cursor()

dir_list = os.listdir(os.path.realpath(TAGSDIR))
print dir_list

