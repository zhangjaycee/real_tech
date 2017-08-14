#!/usr/bin/env python
# coding: utf-8

import os
import re

def proc_name(pathnow):
    flag = False
    print "path:", pathnow
    name_prefix = ''
    max_index = 1
    files = [ f for f in os.listdir(pathnow) if os.path.isfile(os.path.join(pathnow, f)) ]
    #print "files:", files
    for filename in files:
        #print "file: %-30ssize: %d Bytes" % (filename, os.path.getsize(filename))
        m = re.search(r'(.+)_(\d+)\.md', filename)
        if m:
            if not flag:
                flag = True
            max_index = max(max_index, int(m.group(2)))
            if not name_prefix:
                name_prefix = m.group(1)
            #print name_prefix, max_index
    if not flag:
        print "path", pathnow, "is not match"
        return
    max_name = os.path.join(pathnow, '%s_%03d.md' % (name_prefix, max_index))
    new_name = '%s_%03d.md' % (name_prefix, max_index+1)
    create_path = os.path.join(pathnow, new_name)
    create_cmd = 'touch %s' % create_path
    if os.path.getsize(max_name) != 0:
        print "max_name now:", max_name, "size:", os.path.getsize(max_name)
        print "created new file", new_name
        os.system(create_cmd)



if __name__ == "__main__":         
    mypath = "."
    dirs = [ d for d in os.listdir(mypath) if os.path.isdir(os.path.join(mypath,d)) ]
    print "dirs:", dirs

    proc_name(mypath)
    for dirname in dirs:
        proc_name(os.path.join(mypath, dirname))
