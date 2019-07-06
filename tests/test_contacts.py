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
"""dnsgateway client contact management tests."""

from dnsgateway import DnsGatewayClient
from dnsgateway.contact import Contact

import pytest


class TestContacts(object):
    """Test cases for contact management."""

    def test_instance(self, client):
        """Test instantiation."""
        assert isinstance(client, DnsGatewayClient)

    @pytest.mark.parametrize(
        "data",
        ({"id": "TEST", "name": "Test Name", "email": "test@example.com",
          "phone": "+27.110001111", "city": "Test City", "country": "ZA"},)
    )
    def test_create_contact(self, client, data):
        """Test contact creation."""
        contact = client.create_contact(**data)
        assert isinstance(contact, Contact)
        assert isinstance(contact.wid, int)
        for k in ("id", "phone", "email"):
            assert getattr(contact, k) == data[k]
        for address in contact.contact_address:
            assert address["real_name"] == data["name"]
            assert address["city"] == data["city"]
            assert address["country"] == data["country"]

    def test_list_contacts(self, client):
        """Test contact listing."""
        count = 0
        for contact in client.contacts:
            assert isinstance(contact, Contact)
            count += 1
        assert count > 0

    @pytest.mark.parametrize("id", ("TEST",))
    def test_get_contact(self, client, id):
        """Test contact reading."""
        contact = client.contact(id=id)
        assert isinstance(contact, Contact)

    def test_delete_contacts(self, client):
        """Test contact deletion."""
        for contact in client.contacts:
            contact.delete()
        assert len(list(client.contacts)) == 0
