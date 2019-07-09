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

from conftest import CONTACT_DATA

from dnsgateway import DnsGatewayClient
from dnsgateway.contact import Contact

import pytest


@pytest.mark.usefixtures("contact")
class TestContacts(object):
    """Test cases for contact management."""

    def test_instance(self, client):
        """Test instantiation."""
        assert isinstance(client, DnsGatewayClient)

    def test_list_contacts(self, client):
        """Test contact listing."""
        count = 0
        for contact in client.contacts:
            assert isinstance(contact, Contact)
            count += 1
        assert count >= 1

    def test_get_contact(self, client, session_id):
        """Test contact reading."""
        contact = client.contact(id=session_id)
        assert isinstance(contact, Contact)
        assert isinstance(contact.wid, int)
        assert contact.id == session_id
        for k in ("phone", "email"):
            assert getattr(contact, k) == CONTACT_DATA[k]
        for address in contact.contact_address:
            assert address["real_name"] == CONTACT_DATA["name"]
            assert address["city"] == CONTACT_DATA["city"]
            assert address["country"] == CONTACT_DATA["country"]
