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

class ScanManager():
    scanners = []
    scanners_number = 1
    
    def addscanner(self, scanner):
        self.scanners.append(scanner)
        scanner.numtype = self.scanners_number
        self.scanners_number += 1

    def scandir(self, dir):
        global c, TAGSDIR
        for file in os.listdir(os.path.join(TAGSDIR, dir)):
            file_stat = os.stat(os.path.join(TAGSDIR, dir, file))
            file_mtime = file_stat.st_mtime
            file_inode = file_stat.st_ino
            file_db = c.execute("select * from files where inode=? and filename=?", (file_inode, file)).fetchone()
            if file_db:
                if file_db[2] != file_mtime:
                    for scanner in self.scanners:
                        scanner.scanfile(dir, file, file_inode, file_mtime, False)
                else:
                    tag_db = c.execute("update tags set exist=1 where inode=?", (file_inode,))
            else:
                for scanner in self.scanners:
                    scanner.scanfile(dir, file, file_inode, file_mtime, True)
            
            c.execute("update files set exist=1 where inode=? and filename=?", (file_inode, file))

class Filescanner():
    numtype = 0
    def scanfile(self, dir, file, file_inode, file_mtime, create_new):
        pass
    
class TagFileScanner(Filescanner):
    def scanfile(self, dir, file, file_inode, file_mtime, create_new):
        global c
        if create_new:
            print "Adding file:", file
            c.execute("insert into files values(?, ?, ?, ?)", (file_inode, file, file_mtime, 1))
            c.execute("insert into tags values(?, ?, ?, ?)", (file_inode, self.numtype, dir, 1))
        else:
            print "Updating file:", file
            c.execute("update files set mtime=?, exist=1 where inode=?", (file_mtime, file_inode))
            c.execute("update tags set exist=1 where inode=? and type=? and value=?", (file_inode, self.numtype, dir))

try:
    import sqlite3
except:
    print "No sqlite python module found."
    sys.exit(1)

TAGSDIR = os.path.realpath(os.path.expanduser("~/pics"))

conn = sqlite3.connect("pylbooru.db")
c = conn.cursor()

c.execute("update dirs set exist=0")
c.execute("update files set exist=0")
c.execute("update tags set exist=0")

scanmanager = ScanManager()
scanmanager.addscanner(TagFileScanner())

dir_list = os.listdir(TAGSDIR)
for dir in dir_list:
    dir_mtime = os.stat(os.path.join(TAGSDIR, dir)).st_mtime
    dir_db = c.execute("select * from dirs where dirname=?", (dir,)).fetchone()
    if not dir_db:
        print "Adding dir to db:", dir
        c.execute("insert into dirs values(?, ?, ?)", (dir, dir_mtime, 0))
        scanmanager.scandir(dir)
    elif dir_mtime != dir_db[1]:
        print "Updating dir in db:", dir
        c.execute("update dirs set mtime=? where dirname=?", (dir_mtime, dir))
        scanmanager.scandir(dir)
    else:
        c.execute("update files set exist=1 where inode in (select inode from tags where type=1 and value=?)", (dir,))
        c.execute("update tags set exist=1 where inode in (select inode from tags where type=1 and value=?)", (dir,))
        
    c.execute("update dirs set exist=1 where dirname=?", (dir,))

c.execute("delete from dirs where exist=0")
c.execute("delete from files where exist=0")
c.execute("delete from tags where exist=0")

conn.commit()
