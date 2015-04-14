#!/usr/bin/python

# --- INITIALIZATION

from xml.parsers.xmlproc import xmlproc

# --- Interpreting options


# Acting on option settings

    
# --- Starting parse    

def test(c):
    app=xmlproc.Application()
    p=xmlproc.XMLProcessor()
    try:
        p.parse_resource("demo/urls.xml")
        print "PASS"
        return "PASS"
    except:
        print "FAIL"
        return "FAIL"

a=1
test(a)
