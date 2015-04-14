#!/usr/bin/python

#from ddmin import ddmin 

cir=""
open_file=open('demo/urls.xml','r')
for line in open_file:
    cir=cir+line.strip()

open_file.close()
print cir



