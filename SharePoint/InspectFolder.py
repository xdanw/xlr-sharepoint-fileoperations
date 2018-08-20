# Setup
import json
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions
# Not used directly here, but just to be safe
import requests
import requests.utils
# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';

# Extract our configuration items
ci_sourceSite = sourceSite;
ci_tokenServer = sourceSite["tokenServer"];
site_url = ci_sourceSite["url"];
site_site = ci_sourceSite["site"];
site_username = ci_sourceSite["username"];
site_password = ci_sourceSite["password"];

# Trying this because logger seems to be undefined in this context??
global logger
class logger(object):
    @staticmethod
    def info(msg):
        print message;
        return False;

# Here, the ci_sourceSite we get is a hashmap, e.g. we have sourceSite["tokenServer"]
# However, SharePointClient demands attributes, like sourceSite.tokenServer
# So we have to repackage it into a class
# (do not rewrite the other code to use a hashmap, I think ConnectionTest uses attributes)
class sConf(object):
    def __init__(self, tokenServer, url, site):
        self.tokenServer = tokenServer;
        self.url = url;
        self.site = site;

confObject = sConf(ci_tokenServer, site_url, site_site)

# from sharepoint.SharePointClientUtil import SharePoint_Client_Util

# sharepointClient = SharePoint_Client_Util.create_sharepoint_client(confObject, site_username, site_password)
# FormDigestValue = sharepointClient.get_digest()
#     we are going to manually get the digest

# Some more setup
ctx_auth = AuthenticationContext(ci_tokenServer, site_url)
ctx_auth.acquire_token_for_user(site_username, site_password)
request = ClientRequest(ctx_auth)


options = RequestOptions(site_url + "/Sites/" + site_site + "/_api/contextinfo")
options.method = 'POST'
options.set_header('Accept', 'application/json')
options.set_header('Content-Type', 'application/json')
data = request.execute_request_direct(options)
digest = json.loads(data.content)['FormDigestValue']

# If the script has reached this point, our session is authenticated
# Run payload (your desired action) here

# GetFolderByServerRelativeUrl
# print "ServerRequest: " + site_url + "/sites/" + site_site + "/_api/web/GetFolderByServerRelativeUrl('/sites/" + sourceSite + "/" + folderUrl + "')/Files" + " \r\n";
options = RequestOptions(site_url + "/sites/" + site_site + "/_api/web/GetFolderByServerRelativeUrl('/sites/" + sourceSite + "/" + folderUrl + "')/Files")

# Execute
options.method = 'GET'
# Very weird bug. POST method should work, but occasionally gives -1 Invalid request
# when not using command line.
options.set_header('Accept', 'application/json')
options.set_header('Content-Type', 'application/json')
options.set_header('X-RequestDigest',digest)

data = request.execute_request_direct(options)


# List folder objects
responseValue = json.loads(data.content)['value'];
i = 0;
for fileMetadata in responseValue:
    print "[" + str(i) + "]ServerRelativeUrl: " + fileMetadata['ServerRelativeUrl'] + "\r\n";
    i = i + 1;

# Error handling
if "odata.error" in data.content:
    raise Exception;
else:
    print "Success."
