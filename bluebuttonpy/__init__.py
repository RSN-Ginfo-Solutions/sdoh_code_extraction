from bluebuttonpy import documents
from bluebuttonpy.core.core import parse_data
from bluebuttonpy.documents import ccda
from bluebuttonpy.parsers.run import run

"""
Created on Mon Jul  2 21:56:30 2018

@authors: mansooralam, yanjingwang

Modified on Jul 26, 2024:

@author: srikanth235
"""

class CCDA:
    def __init__(self, source, options=None):
        type, parsed_document, parsed_data = None, None, None

        if options is None:
            opts = dict()

        parsed_data = parse_data(source)

        if "parser" in opts:
            parsed_document = opts["parser"]()
        else:
            type = documents.detect(parsed_data)

            if "c32" == type:
                # TODO: add support for legacy C32
                # parsed_data = documents.C32.process(parsed_data)
                # parsed_document = parsers.C32.run(parsed_data)
                pass
            elif "ccda" == type:
                parsed_data = ccda.process(parsed_data)
                parsed_document = run(parsed_data)
            elif "json" == type:
                # TODO: add support for JSON
                pass

        self.type = type
        self.data = parsed_document
        self.source = parsed_data
