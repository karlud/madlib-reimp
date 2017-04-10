#!/usr/bin/env python3
# Story template server

import http.server
import os
from urllib.parse import unquote, parse_qs
from socketserver import ThreadingMixIn

import stories


class StoryHandler(http.server.BaseHTTPRequestHandler):
    '''A request handler that knows about story templates.'''

    # The class variable 'collection' is populated when the server starts.
    collection = None

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        # Pick a random template and make a form with it.
        (num, tmpl) = self.collection.Random()
        hidden = '<input type=hidden name="TEMPLATE" value="{}">\n'.format(num)
        form = tmpl.HTMLForm(hidden)

        self.wfile.write(form.encode())

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

        # TODO: make it HTML instead of text
        self.wfile.write(story.encode())


class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass


if __name__ == '__main__':
    # Get port number from environment if present.
    address = ('', int(os.environ.get('PORT', 8000)))

    # Load the story templates!
    StoryHandler.collection = stories.StoryCollection()

    # Be a server!
    httpd = ThreadHTTPServer(address, StoryHandler)
    httpd.serve_forever()
