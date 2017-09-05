#!/usr/bin/python
"""
Just a small script that renames all the JPEG files
in a folder as 0000.jpg, 0001.jpg etc. Initial order
is retained.
vsbabu AT hotmail DOT com

This is intended as a recipe script, though I use it
way too often to arrange my digital files.

Note that this has possible error conditions that
are not handled at all:
- what if the folder has files already numbered?
- while renaming, it fails if the target file exists

from http://vsbabu.org/webdev/pydev/rename_number.html

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
    print f[0] + "-->" + n
    
    try:
        os.link(f[0], name)
    except:
        print "error: didn't link"