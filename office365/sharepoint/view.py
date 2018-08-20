from office365.runtime.client_object import ClientObject
from office365.runtime.client_query import ClientQuery
from office365.runtime.resource_path_entry import ResourcePathEntry
from office365.sharepoint.view_field_collection import ViewFieldCollection

# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';


class View(ClientObject):
    """Specifies a list view."""

    @property
    def view_fields(self):
        if self.is_property_available('ViewFields'):
            return self.properties['ViewFields']
        else:
            return ViewFieldCollection(self.context, ResourcePathEntry(self.context, self.resource_path, "ViewFields"))

    def delete_object(self):
        """The recommended way to delete a view is to send a DELETE request to the View resource endpoint, as shown
        in View request examples."""
        qry = ClientQuery.delete_entry_query(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
