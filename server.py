#!/usr/bin/env python3
# Story template server

import http.server
import os
from urllib.parse import unquote, parse_qs

import stories

PORT = int(os.environ.get('PORT', 8000))


class StoryHandler(http.server.BaseHTTPRequestHandler):
    collection = None

    def _fieldform(self, field):
        '''Make a form input for a single field.'''
        # Field names start out like '{sport}', so remove the curlies.
        field = field.strip('{}')
        inp = '<label>{}: <input type=text name="{}"></label><br>\n'
        return inp.format(field, field)

    def FieldForm(self):
        '''Make an HTML form for a set of fields.'''
        (num, fields) = self.collection.Random()
        hidden = '<input type=hidden name="TEMPLATE", value="{}">\n'.format(num)
        inputs = [self._fieldform(field) for field in fields]
        head = '<!DOCTYPE html><title>Story Teller</title>\n'
        top = '<form method=POST>\n'
        bottom = '<button type=submit>Tell me a story!</button></form>\n'
        form = head + top + hidden + ''.join(inputs) + bottom
        return form

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(self.FieldForm().encode())

    def do_POST(self):
        # Decode the form fields.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        fieldmap = {}
        tmpl_num = None
        for key, vals in params.items():
            if key == 'TEMPLATE':
                tmpl_num = int(vals[0])
            else:
                # Field names have {curlies} on them, so re-add here.
                fieldmap['{{{}}}'.format(key)] = vals[0]
        story = self.collection.Populate(tmpl_num, fieldmap)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(story.encode())



if __name__ == '__main__':
    address = ('', PORT)
    StoryHandler.collection = stories.StoryCollection()
    httpd = http.server.HTTPServer(address, StoryHandler)
    httpd.serve_forever()
