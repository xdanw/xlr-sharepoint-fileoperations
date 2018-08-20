from office365.runtime.client_object import ClientObject

# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';

class SecurableObject(ClientObject):
    """An object that can be assigned security permissions."""
