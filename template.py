#!/usr/bin/env python3
# template.py - operations on story templates.

import string

class ParseError(Exception):
    '''Error parsing a story template.'''

def FindFields(tmpl):
    '''Extract the fields from the raw text.''' 
    fields = []
    start = 0
    # Read the text, one character at a time.
    # When you see a { for the first time, note its position and keep
    # reading, looking for a closing }.  When you find one, the range
    # from the { to the } is the field.
    for pos, ch in enumerate(tmpl):
        if not start and ch == '{':
            # Start of field.
            start = pos
        elif start and ch == '}':
            # End of field.
            match = tmpl[start:pos+1]
            fields.append((match, start))
            start = 0
            if len(match) < 3:
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
                start, tmpl[start:pos]))
    return fields


def Replace(tmpl, fieldmap):
    '''Replace instances of fields with their corresponding values.
    TODO: This is inefficient; it scans the string once per field.

    Args:
        tmpl: a piece of text with fields in it.
        fieldmap: a dictionary from fields to values.
    '''
    for field, value in fieldmap.items():
        tmpl = tmpl.replace(field, value)
    return tmpl

