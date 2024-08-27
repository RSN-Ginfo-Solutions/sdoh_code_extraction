from bluebuttonpy.core import wrappers
from bluebuttonpy.core.core import strip_whitespace

"""
Created on Mon Jul  2 21:23:37 2018

@author: mansooralam, yanjingwang

Modified on Jul 26, 2024:

@author: srikanth235
"""

"""
Parser for any freetext section (i.e., contains just a single <text> element)
"""


def free_text(ccda, section_name):
    doc = ccda.section(section_name)
    text = strip_whitespace(doc.tag("text").val())

    return wrappers.ObjectWrapper(text=text)
