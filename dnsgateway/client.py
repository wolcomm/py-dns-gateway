# Copyright (c) 2019 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""dnsgateway.client module."""

import logging

import requests

log = logging.getLogger(__name__)

PRODUCTION_ENDPOINT = "https://gateway-epp.dns.net.za/api"
DEVELOPMENT_ENDPOINT = "https://gateway-otande.dns.net.za:8443/api"


class DnsGatewayClient(object):
    """DNS Gateway API client implementation."""

    def __init__(self, endpoint=PRODUCTION_ENDPOINT, user=None, token=None):
        """Initialise a new client instance."""
        self.endpoint = endpoint
        self.auth = (user, token)

    def _get(self, path=None):
        url = f"{self.endpoint}/{path}"
        try:
            resp = requests.get(url, auth=self.auth)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            log.error(e)
            raise e

    @property
    def domains(self):
        """Get a list of registered domains."""
        path = "registry/domains"
        data = self._get(path=path)
        return data["results"]

    @property
    def contacts(self):
        """Get a list of registered contacts."""
        path = "registry/contacts"
        data = self._get(path=path)
        return data["results"]
