from office365.runtime.client_object_collection import ClientObjectCollection

# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';

class ContentTypeCollection(ClientObjectCollection):
    """Content Type resource collection"""
