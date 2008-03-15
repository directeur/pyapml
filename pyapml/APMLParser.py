#!/usr/bin/env python
"""APML parser

Parses an apml XML file/stream/string and generate 
a Pythonic object representation of it.

Visit http://xhtml-css.com/blog/python/pyapml 
for the doc and thelatest version

"""

from pyapml.toolbox import openAnything, xml2obj


def list_please(obj):
    """ returns allways a list """
    
    if isinstance(obj, list):
        return obj 
    else:
        return [obj]    


class Attention(object):
    """ defines an elementary attention (concepts and sources) """
    
    def __init__(self, data):
        
        Concepts = getattr(data, 'Concepts', [])
        Sources = getattr(data, 'Sources', [])
        self.concepts = list_please(getattr(Concepts, 'Concept', []))    
        self.sources = list_please(getattr(Sources, 'Source', []))
        # convert value to floats
        for c in self.concepts:
            c.value = float(c.value)


class Profile(object):
    """ defines an apml profile """

    def __init__(self, xml_profile):
        self.name = xml_profile.name

        xml_implicitdata = getattr(xml_profile, 'ImplicitData', [])
        xml_explicitdata = getattr(xml_profile, 'ExplicitData', [])
        self.implicit = Attention(xml_implicitdata)
        self.explicit = Attention(xml_explicitdata)


class Apml(object):
    """ defines a generic apml object """

    def __init__(self, xml_obj=None):
        
        self.head = xml_obj.Head
        self.body = xml_obj.Body
        self.profiles = [Profile(P) for P in xml_obj.Body.Profile]

    def get_all_concepts(self):
        """ get all the defined concepts """

        concepts = []
        for profile in self.profiles:
            concepts = concepts+profile.implicit.concepts
            concepts = concepts+profile.explicit.concepts
        return concepts


    def get_all_sources(self):
        """ get all the defined sources """

        sources = []
        for profile in self.profiles:
            sources = sources+profile.implicit.sources
            sources = sources+profile.explicit.sources
        return sources
            


class APMLParser(object):
    """  a class that handles parsing of apml sources """
    
    def __init__(self, source):
        self.apml_source = source
        self.apml_content = openAnything(source).read()


    def parse (self):
        """ Parses an apml file and returns an apml object """

        xmlobj = xml2obj(self.apml_content)

        # create a structure similar to the one 
        # defined by Jon Ciancillo in his php version.           
        return Apml(xmlobj)


if __name__ == "__main__":
    parser = APMLParser("test.apml")
    a = parser.parse()

    print "%s Concepts"% a.profiles[0].name
    for c in a.profiles[0].implicit.concepts:
        print "Concept: %s ==> Value: %s"%(c.key, c.value)


