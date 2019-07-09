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
"""dnsgateway client domain management tests."""

from dnsgateway import DnsGatewayClient
from dnsgateway.domain import Domain

import pytest

ZONES = ("com", "co.za", "africa")
HOSTS = ("ns.example.com", "ns.example.net")


class TestDomains(object):
    """Test cases for domain management."""

    def test_instance(self, client):
        """Test instantiation."""
        assert isinstance(client, DnsGatewayClient)

    @pytest.mark.parametrize("zone", ZONES)
    def test_create_domain(self, client, session_id, zone, contact):
        """Test domain creation."""
        name = f"py-dns-gateway-{session_id}.{zone}"
        contacts = {k: contact.id
                    for k in ("registrant", "admin", "billing", "tech")}
        charge = client.check_domain(name=name)
        assert charge is not False
        domain = client.create_domain(name=name, hosts=HOSTS,
                                      charge=charge, **contacts)
        assert isinstance(domain, Domain)
        assert isinstance(domain.wid, int)
        assert domain.name == name
        assert domain.zone == zone

    def test_list_domains(self, client):
        """Test domain listing."""
        count = 0
        for domain in client.domains:
            assert isinstance(domain, Domain)
            count += 1
        assert count >= len(ZONES)

    @pytest.mark.parametrize("zone", ZONES)
    def test_get_domain(self, client, session_id, zone):
        """Test domain reading."""
        name = f"py-dns-gateway-{session_id}.{zone}"
        domain = client.domain(name=name)
        assert isinstance(domain, Domain)
        assert isinstance(domain.wid, int)
        assert domain.name == name
        assert domain.zone == zone

    @pytest.mark.parametrize("zone", ZONES)
    def test_delete_domain(self, client, session_id, zone, contact):
        """Test domain deletion."""
        name = f"py-dns-gateway-{session_id}.{zone}"
        domain = client.domain(name=name)
        domain.delete()
