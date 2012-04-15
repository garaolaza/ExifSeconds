#!/usr/bin/python

#    Copyright 2011 Gari Araolaza gari@eibar.org
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


# HTC Tattoo's timestamps are buggy. This program
# solves this problem in your photos
# 
# Dependencies: You will need pyexiv2 library (v 3.0 )installed on your system to run it
#
#
# Usage:  python exifseconds.py <PATH_TO_FIX_FILES>
#
# Please give feedback if you find something could be better in this script.
# gari@eibar.org
 

import sys, os
import pyexiv2
import re
from datetime import datetime

pattext = "[0-9][0-9][0-9][0-9]:[0-9][0-9]:[0-9][0-9]\ [0-9][0-9]:[0-9][0-9]$"
pattern = re.compile(pattext)

def get_images_from_path(basepath):
    image_list = []
    for root, subdirs, files in os.walk(basepath):
        for file in files:
            if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
                image_list.append(os.path.join(root, file))
    return image_list          

def fix_date_time(image_path):
    metadata = pyexiv2.ImageMetadata(image_path)
    metadata.read()
    try:
        tag = metadata['Exif.Photo.DateTimeOriginal']
        raw = tag.raw_value
    except:
        tag = None
            
    if type(raw)==type('') and pattern.match(raw):
        corrected_string = "%s:00" % raw
        corrected_datetime = datetime.strptime(corrected_string, '%Y:%m:%d %H:%M:%S')          
        tag.value = corrected_datetime #now in datetime format!
        metadata.write()
        print image_path.split('/')[-1], 'Fixed'
        print '', raw
        print '', corrected_datetime
       
       
def main(argv):
    if len(argv)<2:
        print """This program fixes invalid DateTime stamps, 
adding 00 seconds to the date. Specially created to be used
with pictures from the HTC Tattoo."""
        return 
    
    image_list = get_images_from_path(argv[1])       
    
    for image_path in image_list:
        fix_date_time(image_path)
        

if __name__ == "__main__":
    main(sys.argv)