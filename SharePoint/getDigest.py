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

def getDigest(url, username, password, site=None):
#   url = 'https://xebialabs.sharepoint.com/sites/TestCommunicationSite'
    if site:
        url = "%s/sites/%s" % (url, site)
    ctx_auth = AuthenticationContext(url)
    if ctx_auth.acquire_token_for_user(username, password):
        request = ClientRequest(ctx_auth)
        options = RequestOptions("{0}/_api/contextinfo".format(url))
        options.method = 'POST'
        options.set_header('Accept', 'application/json')
        options.set_header('Content-Type', 'application/json')
        data = request.execute_request_direct(options)
        digest = json.loads(data.content)['FormDigestValue']
        return digest
    else:
        return "Failed to acquire authentication token"

if __name__ == "__main__":
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    if len(sys.argv) > 4:
        site = sys.argv[4]
    else:
        site = None
    print getDigest(url, username, password, site)
