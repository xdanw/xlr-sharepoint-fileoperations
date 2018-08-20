#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import json
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions

class SharePoint_Client(object):
    def __init__(self, configuration, username, password):
        # logger.info("Initializing SharePoint_Client object")
        print("Initializing SharePoint_Client object")
        self.tokenServer = configuration.tokenServer
        self.url = configuration.url
        self.site = configuration.site

        if self.site:
            self.url = "%s/sites/%s" % (self.url, self.site)
        if username:
            self.username = username
        else:
            self.username = configuration.username
        if password:
            self.password = password
        else:
            self.password = configuration.password
        # logger.info("Exiting __init__()")
        print("Exiting __init__()")

    @staticmethod
    def create_sharepoint_client(configuration, username=None, password=None):
        return SharePoint_Client(configuration, username, password)

    def get_digest(self):
        # logger.info("Executing get_digest()")
        print("Executing get_digest()")
        # logger.info("url %s" % self.url)
        # logger.info("username %s" % self.username)
        # logger.info("password %s" % self.password)
        ctx_auth = AuthenticationContext(self.tokenServer, self.url)
        if ctx_auth.acquire_token_for_user(self.username, self.password):
            request = ClientRequest(ctx_auth)
            options = RequestOptions("{0}/_api/contextinfo".format(self.url))
            options.method = 'POST'
            options.set_header('Accept', 'application/json')
            options.set_header('Content-Type', 'application/json')
            data = request.execute_request_direct(options)
            if "odata.error" in data.content:
                self.throw_error(data.content['odata.error']['message']['value'])
            else:
                return json.loads(data.content)['FormDigestValue']
        else:
            self.throw_error("Failed to acquire authentication token for %s" % self.url)

    def throw_error(self, errmsg):
        # logger.info("Error from SharePoint, %s" % errmsg)
        print "Error from SharePoint, %s\n" % errmsg
        sys.exit(1)
