#!/usr/bin/env python

from pyapml.APMLParser import APMLParser

def main():
    parser = APMLParser('test.apml')
    apml = parser.parse()

   
    print '=========================================='

    print "APML Title: %s" % apml.head.Title

    print "%s Implicit Concepts" % apml.profiles[0].name
    for c in apml.profiles[0].implicit.concepts:
        print "Concept: %s ==> Value: %s"%(c.key, c.value)

    print "%s Explicit Concepts" % apml.profiles[0].name
    for c in apml.profiles[0].explicit.concepts:
        print "Concept: %s ==> Value: %s"%(c.key, c.value)


    print '=========================================='
    print '              ALL CONCEPTS'
    print '=========================================='

    allconcepts = apml.get_all_concepts()

    for c in allconcepts:
        print "Concept: %s ==> Value: %s"%(c.key, c.value)

if __name__ == "__main__":
    main()
