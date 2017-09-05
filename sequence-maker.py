#!/usr/bin/python
"""
Script that takes a dump of jpeg images from a GPS enabled camera
and outputs them as a long sequence starting with 0000001.jpg

Inspired http://vsbabu.org/webdev/pydev/rename_number.html

Copyright (C) 2017 Mishari Muqbil

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

"""
import string
import os
import exifread
import fnmatch
import argparse
from operator import itemgetter

filedate = []

def walk_directory(source_dir):
    for root, dirnames, filenames in os.walk(source_dir):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            yield os.path.join(root, filename)
            
parser = argparse.ArgumentParser()
parser.add_argument('src', help="source directory")
parser.add_argument('dest', help="destination directory")
args = parser.parse_args()


source_dir = args.src
dest_dir = args.dest

# and rename each file
for i,f in enumerate(walk_directory(source_dir)):
    
    z = open(f, 'rb')
    
    tags = exifread.process_file(z, details=False)
    
    z.close()

    # for tag in tags:
    #     print tag
    # exit()

    try:
        # This is theoretical, need to check if it works.
        tags["GPS GPSVersionID"]
        filedate.append( ( f, str(tags["Image DateTime"] )) )
    except KeyError:
        print "No GPS tags"
        
filedate = sorted(filedate, key=itemgetter(1), reverse=False)

for i,f in enumerate(filedate):
    name = string.zfill(i+1,7) + ".jpg"
    print f[0] + " --> " + name
    
    try:
        os.link(f[0], name)
    except:
        print "error: didn't link"
