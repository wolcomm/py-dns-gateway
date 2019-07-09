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
"""dnsgateway test fixtures."""

import json
import os
import uuid

import click.testing

from dnsgateway import DnsGatewayClient
from dnsgateway.client import DEVELOPMENT_ENDPOINT
from dnsgateway.contact import Contact

import pytest

import requests.exceptions

CONTACT_DATA = {"name": "Test Contact", "email": "test@example.com",
                "phone": "+27.110001111", "city": "Test City",
                "country": "ZA"}


@pytest.fixture(scope="session")
def session_id():
    """Generate a unique session id."""
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def credentials():
    """Get credentials for the development environment."""
    credentials_path = os.path.join(os.path.dirname(__file__),
                                    "credentials.json.secret")
    with open(credentials_path) as f:
        credentials = json.load(f)
    return credentials


@pytest.fixture(scope="session")
def client(credentials):
    """Get an instance of DnsGatewayClient as a test fixture."""
    api_client = DnsGatewayClient(endpoint=DEVELOPMENT_ENDPOINT, **credentials)
    return api_client


@pytest.fixture(scope="class")
def contact(client, session_id):
    """Create a test contact."""
    contact = client.create_contact(id=session_id, **CONTACT_DATA)
    assert isinstance(contact, Contact)
    assert isinstance(contact.wid, int)
    assert contact.id == session_id
    for k in ("phone", "email"):
        assert getattr(contact, k) == CONTACT_DATA[k]
    for address in contact.contact_address:
        assert address["real_name"] == CONTACT_DATA["name"]
        assert address["city"] == CONTACT_DATA["city"]
        assert address["country"] == CONTACT_DATA["country"]
    yield contact
    try:
        contact.delete()
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 400
        assert e.response.json()["detail"] == \
            "Domain dependencies prohibit contact 'delete' operation"
    return


@pytest.fixture()
def cli():
    """Get a click CliRunner."""
    return click.testing.CliRunner()
