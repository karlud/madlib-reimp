#!/usr/bin/env python3
# template.py - operations on story templates.

import string

class ParseError(Exception):
    '''Error parsing a story template.'''

def FindFields(text):
    '''Extract the fields from the raw text.''' 
    fields = []
    start = 0
    # Read the text, one character at a time.
    # When you see a { for the first time, note its position and keep
    # reading, looking for a closing }.  When you find one, the range
    # from the { to the } is the field.
    for pos, ch in enumerate(text):
        if not start and ch == '{':
            # Start of field.
            start = pos
        elif start and ch in string.whitespace:
            # No whitespace in field names.
            raise ParseError("Whitespace in field name at offset {}".format(pos))
        elif start and ch == '}':
            # End of field.
            match = text[start+1:pos]
            fields.append((match, start))
            start = 0
            if len(match) < 1:
                # Fields can't have empty names.
                raise ParseError("Empty field at offset {}".format(pos))
        elif not start and ch == '}':
            # We saw a } with no { before it.  That's an error.
            raise ParseError(
                "}} with no matching {{ at offset {}.".format(pos))
    if start:
        # We saw a { and then got to the end of the string with no }.
        raise ParseError(
            "Field began line at offset {} but didn't end: {}".format(
                start, text[start:pos]))
    return fields
