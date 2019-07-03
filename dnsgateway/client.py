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

from dnsgateway.contact import Contact
from dnsgateway.domain import Domain
from dnsgateway.zone import Zone

log = logging.getLogger(__name__)

PRODUCTION_ENDPOINT = "https://gateway-epp.dns.net.za/api"
DEVELOPMENT_ENDPOINT = "https://gateway-otande.dns.net.za:8443/api"


class DnsGatewayClient(object):
    """DNS Gateway API client implementation."""

    def __init__(self, endpoint=PRODUCTION_ENDPOINT,
                 username=None, password=None):
        """Initialise a new client instance."""
        log.debug(f"Setting endpoint: {endpoint}")
        self.endpoint = endpoint
        log.debug(f"Setting authentication username: {username}")
        self.auth = (username, password)

    def _get(self, path=None, params=None):
        if path.startswith("https://"):
            url = path
        else:
            url = f"{self.endpoint}/{path}"
        log.debug(f"trying to GET {url}")
        try:
            resp = requests.get(url, auth=self.auth, params=params)
        except Exception as e:
            log.error(e)
            raise e
        try:
            data = resp.json()
        except Exception as e:
            log.error(e)
            raise e
        try:
            resp.raise_for_status()
        except Exception as e:
            log.error(f"{e}: {data.get('detail')}")
            raise e
        return data

    def _get_iter(self, path=None, params=None):
        next = path
        while next is not None:
            data = self._get(path=next, params=params)
            log.debug(f"Got data: {data}")
            next = data["next"]
            yield data

    @property
    def domains(self):
        """Get a list of registered domains."""
        log.debug("Trying to get registered domains")
        path = "registry/domains"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Domain(client=self, **result)

    def domain(self, id=None, name=None):
        """Get a domain by id or name."""
        if id and name:
            err = RuntimeError("specify only one of 'id' or 'name'")
            log.error(err)
            raise err
        if id:
            log.debug(f"Trying to get domain by id '{id}'")
            path = f"registry/domains/{id}"
            data = self._get(path=path)
            return Domain(client=self, **data)
        if name:
            log.debug(f"Trying to get domain by name '{name}'")
            path = "registry/domains"
            params = {"name": name}
            data = self._get(path=path, params=params)
            if data["count"] != 1:
                err = RuntimeError(f"got {data['count']} results")
                log.error(err)
                raise err
            return Domain(client=self, **data["results"][0])

    @property
    def contacts(self):
        """Get a list of registered contacts."""
        log.debug("Trying to get registered contacts")
        path = "registry/contacts"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Contact(client=self, **result)

    def contact(self, id=None):
        """Get a contact by id."""
        if id:
            log.debug(f"Trying to get contact by id '{id}'")
            path = "registry/contacts"
            params = {"id": id}
            data = self._get(path=path, params=params)
            if data["count"] != 1:
                err = RuntimeError(f"got {data['count']} results")
                log.error(err)
                raise err
            return Contact(client=self, **data["results"][0])

    @property
    def zones(self):
        """Get list of supported zones."""
        log.debug("Trying to get supported zones")
        path = "registry/zones"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Zone(client=self, **result)
