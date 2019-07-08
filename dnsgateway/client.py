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

    def _request(self, method="GET", path=None, params=None, data=None):
        if path.startswith("https://"):
            url = path
        else:
            url = f"{self.endpoint}/{path}"
        log.debug(f"Trying HTTP {method} to {url}")
        try:
            resp = requests.request(method, url, auth=self.auth,
                                    params=params, json=data)
        except Exception as e:
            log.error(e)
            raise e
        log.debug(f"Got response {resp.status_code}: {resp.reason}")
        log.debug(f"Response headers: {resp.headers}")
        try:
            resp.raise_for_status()
        except Exception as e:
            try:
                error_details = resp.json()
            except Exception:
                error_details = None
            log.error(f"{e}: {error_details}")
            raise e
        try:
            data = resp.json()
        except Exception as e:
            log.error(e)
            raise e
        return data

    def _get(self, path=None, params=None):
        return self._request(method="GET", path=path, params=params)

    def _post(self, path=None, data=None):
        return self._request(method="POST", path=path, data=data)

    def _put(self, path=None, data=None):
        return self._request(method="PUT", path=path, data=data)

    def _delete(self, path=None):
        return self._request(method="DELETE", path=path)

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
        path = f"{Domain.base_path}/"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Domain(client=self, **result)

    def domain(self, wid=None, name=None):
        """Get a domain by wid or name."""
        if wid and name:
            log.debug(f"wid:{wid} name:{name}")
            err = RuntimeError("specify only one of 'wid' or 'name'")
            log.error(err)
            raise err
        if wid:
            log.debug(f"Trying to get domain by wid '{wid}'")
            path = f"{Domain.base_path}/{wid}"
            data = self._get(path=path)
            return Domain(client=self, **data)
        if name:
            log.debug(f"Trying to get domain by name '{name}'")
            path = f"{Domain.base_path}/"
            params = {"name": name}
            data = self._get(path=path, params=params)
            if data["count"] != 1:
                err = RuntimeError(f"got {data['count']} results")
                log.error(err)
                raise err
            return Domain(client=self, **data["results"][0])

    def check_domain(self, name=None, op="create"):
        """Check domain name availability."""
        log.debug(f"Checking availability of domain name {name} for {op}")
        path = f"{Domain.base_path}/check/"
        details = {"name": name}
        log.debug(f"Check details: {details}")
        data = self._post(path=path, data=details)
        log.debug(f"Result: {data}")
        if int(data["results"][0]["avail"]):
            try:
                return data["charge"]["action"][op]
            except KeyError as e:
                log.error(e)
                raise e
        else:
            return False

    def create_domain(self, name=None, period=1, period_unit="y",
                      autorenew=False, authinfo="coza", hosts=[], charge=None,
                      admin=None, registrant=None, billing=None, tech=None):
        """Create a domain."""
        log.debug(f"Trying to create domain {name}")
        path = f"{Domain.base_path}/"
        kwargs = locals()
        details = {
            "name": name,
            "period": period,
            "period_unit": period_unit,
            "autorenew": autorenew,
            "authinfo": authinfo,
            "hosts": [{"hostname": host} for host in hosts],
            "contacts": [{"type": t, "contact": {"id": kwargs[t]}}
                         for t in ("registrant", "admin", "billing", "tech")]
        }
        if charge is not None:
            details["charge"] = {"price": charge}
        log.debug(f"Domain details: {details}")
        data = self._post(path=path, data=details)
        return Domain(client=self, **data)

    @property
    def contacts(self):
        """Get a list of registered contacts."""
        log.debug("Trying to get registered contacts")
        path = f"{Contact.base_path}/"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Contact(client=self, **result)

    def contact(self, id=None):
        """Get a contact by id."""
        if id:
            log.debug(f"Trying to get contact by id '{id}'")
            path = f"{Contact.base_path}/"
            params = {"id": id}
            data = self._get(path=path, params=params)
            if data["count"] != 1:
                err = RuntimeError(f"got {data['count']} results")
                log.error(err)
                raise err
            return Contact(client=self, **data["results"][0])

    def create_contact(self, id=None, name=None, org=None,
                       email=None, phone=None, fax=None,
                       address1=None, address2=None, address3=None,
                       city=None, province=None, code=None, country=None):
        """Create a contact."""
        log.debug("Trying to create a new contact")
        path = f"{Contact.base_path}/"
        details = {
            "id": id,
            "phone": phone,
            "fax": fax,
            "email": email,
            "contact_address": [
                {
                    "real_name": name,
                    "org": org,
                    "address1": address1,
                    "address2": address2,
                    "address3": address3,
                    "city": city,
                    "province": province,
                    "code": code,
                    "country": country,
                    "type": type
                } for type in ("loc", "int")
            ]
        }
        log.debug(f"Contact details: {details}")
        data = self._post(path=path, data=details)
        return Contact(client=self, **data)

    @property
    def zones(self):
        """Get list of supported zones."""
        log.debug("Trying to get supported zones")
        path = f"{Zone.base_path}/"
        for data in self._get_iter(path=path):
            for result in data["results"]:
                yield Zone(client=self, **result)
