from office365.runtime.client_object_collection import ClientObjectCollection

# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';


class ViewFieldCollection(ClientObjectCollection):
    """Represents a collection of View resources."""

    def __init__(self, context, resource_path=None):
        super(ViewFieldCollection, self).__init__(context, resource_path)
        self.use_custom_mapper = True

    def map_json(self, payload):
        super(ViewFieldCollection, self).map_json(payload)
