#!/usr/bin/env python3
#
# Operations on story templates, including loading them from files on disk.

import os
import random


class ParseError(Exception):
    '''Error parsing a story template.'''


class StoryTemplate(object):
    def __init__(self, text=None, fname=None):
        if fname is not None:
            self.text = open(fname).read()
        elif text is not None:
            self.text = text
        else:
            raise ParseError("StoryTemplate needs text or a filename.")
        self.fields = self._FindFields(self.text)
        if len(self.fields) == 0:
            raise ParseError("Story template should have at least one field.")

    def _FindFields(self, tmpl):
        '''Extract field names from a story template string.

        Args:
            tmpl: a string containing template fields in {curlies}.

        Returns:
            A set of field names, e.g. {'{curlies}'}.
        '''
        fields = set()
        start = None
        # Read the text, one character at a time.
        # When you see a { for the first time, note its position and keep
        # reading, looking for a closing }.  When you find one, the range
        # from the { to the } is the field.
        for pos, ch in enumerate(tmpl):
            if start is None and ch == '{':
                # Start of field.
                start = pos
            elif start is not None and ch == '}':
                # End of field.
                match = tmpl[start:pos+1]
                if len(match) < 3:
                    # Fields can't have empty names.
                    raise ParseError("Empty field at offset {}".format(pos))
                fields.add(match)
                start = None
            elif start is None and ch == '}':
                # We saw a } with no { before it.  That's an error.
                raise ParseError(
                    "}} with no matching {{ at offset {}.".format(pos))
        if start:
            # We saw a { and then got to the end of the string with no }.
            raise ParseError(
                "Field began at offset {} but didn't end: {}".format(
                    start, tmpl[start:pos]))
        return fields

    def Populate(self, fieldmap):
        '''Return a populated version of this story, given particular fields.

        Args:
            fieldmap: a dictionary from fields to values.

        Returns:
            string: a filled-in version of the story.
        '''
        text = self.text
        for field, value in fieldmap.items():
            text = text.replace(field, value)
        return text

    def _fieldform(self, field):
        '''Make a form input for a single field.'''
        # Field names start out like '{sport}', so remove the curlies.
        field = field.strip('{}')
        inp = '<label>{}: <input type=text name="{}"></label><br>'
        return inp.format(field, field)

    def HTMLForm(self, hidden=''):
        '''Return an HTML form for this story.

        Args:
            hidden: optional hidden field (or anything else)

        Returns:
            string: an HTML document of a form.
        '''
        doc = ('<!DOCTYPE html>\n'
               '<title>Story</title>\n'
               '<form method=POST>\n{}\n'
               '<button type=submit>Tell me a story!</button>\n'
               '</form>')
        inputs = [self._fieldform(field) for field in self.fields]
        inputs.append(hidden)
        return doc.format('\n'.join(inputs))


class StoryCollection(object):
    def __init__(self, dirname="stories"):
        self.templates = self._LoadDirectory(dirname)

    def _LoadDirectory(self, dirname):
        '''Load story templates from a directory.

        Args:
            dirname: the name of a directory to find story files in.

        Returns:
            A list of StoryTemplate objects.
        '''
        templates = []
        for fname in os.listdir(dirname):
            try:
                tmpl = StoryTemplate(fname=os.path.join(dirname, fname))
                templates.append(tmpl)
            except ParseError:
                print("File {} didn't parse!".format(fname))
                raise
        return templates

    def Random(self):
        '''Return a random template number and template.'''
        num = random.randint(0, len(self.templates) - 1)
        return (num, self.templates[num])

    def Populate(self, num, fieldmap):
        '''Return a populated story from template #num.'''
        return self.templates[num].Populate(mieldmap)
