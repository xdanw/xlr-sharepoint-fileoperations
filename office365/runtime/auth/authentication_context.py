from office365.runtime.auth.acs_token_provider import ACSTokenProvider
from office365.runtime.auth.base_authentication_context import BaseAuthenticationContext
from office365.runtime.auth.saml_token_provider import SamlTokenProvider

# Fixes some issues with TLS
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';

class AuthenticationContext(BaseAuthenticationContext):
    """Authentication context for SharePoint Online/One Drive"""

    def __init__(self, tokenServer, url):
        super(AuthenticationContext, self).__init__()
        self.tokenServer = tokenServer
        self.url = url
        self.provider = None

    def acquire_token_for_user(self, username, password):
        """Acquire token via user credentials"""
        # logger.info("Executing acquire_token_for_user() %s %s" % (username, password))
        # print("Executing acquire_token_for_user() %s %s %s %s" % (self.tokenServer, self.url, username, password))
        self.provider = SamlTokenProvider(self.tokenServer, self.url, username, password)
        # logger.info("Exiting acquire_token_for_user()")
        # print("Exiting acquire_token_for_user()")
        return self.provider.acquire_token()

    def acquire_token_for_app(self, client_id, client_secret):
        """Acquire token via client credentials"""
        # logger.info("Executing acquire_token_for_app() %s %s" % (client_id, client_secret))
        # print("Executing acquire_token_for_app() %s %s" % (client_id, client_secret))
        self.provider = ACSTokenProvider(self.url, client_id, client_secret)
        # logger.info("Exiting acquire_token_for_app()")
        # print("Exiting acquire_token_for_app()")
        return self.provider.acquire_token()

    def authenticate_request(self, request_options):
        """Authenticate request"""
        # logger.info("Executing authenticate_request()")
        # print("Executing authenticate_request()")
        if isinstance(self.provider, SamlTokenProvider):
            request_options.set_header('Cookie', self.provider.get_authentication_cookie())
        elif isinstance(self.provider, ACSTokenProvider):
            request_options.set_header('Authorization', self.provider.get_authorization_header())
        else:
            raise ValueError('Unknown authentication provider')
        # logger.info("Exiting authenticate_request()")
        print("Exiting authenticate_request()")

    def get_auth_url(self, redirect_url):
        return ""

    def get_last_error(self):
        return self.provider.get_last_error()
