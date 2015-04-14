#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from split import split
from listsets import listminus
import re
from xml.parsers.xmlproc import xmlproc
import sys,outputters,getopt

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances

def test(c):
    global counter
    counter=counter+1
    app=xmlproc.Application()
    warnings=1
    entstack=0
    rawxml=0
    p=xmlproc.XMLProcessor()
    err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)
    temp_str=""
    for i in range(len(c)):
        temp_list=list(c[i])
        temp_str=temp_str+temp_list[1]
    output_file=open('mypython.xml','w')
    output_file.write(temp_str)
    output_file.close()
    try:
        p.parse_resource('mypython.xml')
        p.reset()
        return PASS
    except UnboundLocalError:
        return FAIL

if __name__ == "__main__":
    tests = {}
    circumstances = []

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    def mytest(c):
        global tests
        global circumstances

        s = ""
        for (index, char) in c:
            s += char

        if s in tests.keys():
            return tests[s]

        map = {}
        for (index, char) in c:
            map[index] = char

        x = ""
        for i in range(len(circumstances)):
            if map.has_key(i):
                x += map[i]
            else:
                x += "."

        print "%02i" % (len(tests.keys()) + 1), "Testing", `x`,

        
        if s != "" and re.match("<SELECT.*>", s):
            print FAIL
            tests[s] = FAIL
            return FAIL
        print PASS
        tests[s] = PASS
        return PASS

    counter=0
    cir=""
    open_file=open('demo/urls.xml','r')
    for line in open_file:
        cir=cir+line#.strip()
    open_file.close()

    circumstances = string_to_list(cir)
    print ddmin(circumstances, test)
    print "counter : " + str(counter)
    #print ddmin(cir, test)

