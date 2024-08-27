import json as std_json
import logging

from bluebuttonpy.core import xml

"""
Created on Mon Jul  2 21:43:56 2018

@author: mansooralam, yanjingwang

Modified on Jul 26, 2024:

@author: srikanth235
"""



# Initialize the logging module
logging.getLogger(__name__).addHandler(logging.NullHandler())


def strip_whitespace(text):
    """Remove leading and trailing whitespace from a string"""

    if not isinstance(text, str):
        return text
    return text.strip()

def json():
    raise NotImplementedError()


def parse_data(source):
    source_stripped = strip_whitespace(source)

    if source_stripped.startswith("<?xml"):
        return xml.parse(source)

    try:
        return std_json.loads(source)
    except:
        logging.error(
            "Error: Cannot parse this file. BB.js only accepts valid XML (for "
            "parsing) or JSON (for generation). If you are attempting to "
            "provide XML or JSON, please run your data through a validator to "
            "see if it is malformed.\n"
        )
        raise


def trim():
    # I don't think this is needed with the standard JSONEncoder
    raise NotImplementedError()
