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
"""dnsgateway cli tests."""

from unittest.mock import DEFAULT, PropertyMock, patch

from dnsgateway.__meta__ import __version__ as version
from dnsgateway.cli import main

import pytest

DOMAIN = "<DOMAIN>"
DOMAINS = (DOMAIN,)
NAME = "example.com"
CHARGE = "<CHARGE>"

CONTACT = "<CONTACT>"
CONTACTS = (CONTACT,)
CONTACT_ID = "TEST"

ZONE = "<ZONE>"
ZONES = (ZONE,)


class TestCli(object):
    """Test cases for cli tool."""

    def _check_result(self, value, exc, result):
        if exc is Exception:
            assert result.exit_code == 1
        else:
            assert result.exit_code == 0
            assert result.output.rstrip() == value
        return True

    def test_help(self, cli):
        """Test cli help."""
        result = cli.invoke(main, "--help")
        assert result.exit_code == 0
        assert result.output.startswith("Usage:")

    def test_version(self, cli):
        """Test cli version."""
        result = cli.invoke(main, "--version")
        assert result.exit_code == 0
        assert result.output.rstrip().endswith(version)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_domain_list(self, cli, credentials, exc):
        """Test domain list command."""
        with patch("dnsgateway.cli.DnsGatewayClient.domains",
                   new_callable=PropertyMock) as m:
            m.return_value = DOMAINS
            m.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "domain", "list"))
            m.assert_called_once_with()
        assert self._check_result(DOMAIN, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_domain_show(self, cli, credentials, exc):
        """Test domain show command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            client.domain.return_value = DOMAIN
            client.domain.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "domain", "show", NAME))
            client.domain.assert_called_once_with(name=NAME)
        assert self._check_result(DOMAIN, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_domain_check(self, cli, credentials, exc):
        """Test domain check command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            client.check_domain.return_value = CHARGE
            client.check_domain.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "domain", "check", NAME))
            client.check_domain.assert_called_once_with(name=NAME, op="create")
        assert self._check_result(CHARGE, exc, result)

    @pytest.mark.parametrize("exc_check", ((DEFAULT,), Exception))
    @pytest.mark.parametrize("exc_create", ((DEFAULT,), Exception))
    def test_domain_create(self, cli, credentials, exc_check, exc_create):
        """Test domain create command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            client.check_domain.return_value = CHARGE
            client.check_domain.side_effect = exc_check
            client.create_domain.return_value = DOMAIN
            client.create_domain.side_effect = exc_create
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "domain", "create",
                                       "--name", NAME, "-y",
                                       "--admin", CONTACT_ID,
                                       "--registrant", CONTACT_ID,
                                       "--billing", CONTACT_ID,
                                       "--tech", CONTACT_ID))
            client.check_domain.assert_called_once_with(name=NAME, op="create")
            if exc_check is not Exception:
                client.create_domain.assert_called_once_with(name=NAME,
                                                             charge=CHARGE,
                                                             period=1,
                                                             autorenew=False,
                                                             hosts=(),
                                                             admin=CONTACT_ID,
                                                             registrant=CONTACT_ID,  # noqa: E501
                                                             billing=CONTACT_ID,  # noqa: E501
                                                             tech=CONTACT_ID)
        if exc_check is Exception or exc_create is Exception:
            exc = Exception
        else:
            exc = None
        assert self._check_result(DOMAIN, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_domain_delete(self, cli, credentials, exc):
        """Test domain delete command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            domain = client.domain.return_value
            domain.delete.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "domain", "delete", NAME))
            client.domain.assert_called_once_with(name=NAME)
            domain.delete.assert_called_once_with()
        assert self._check_result(f"Domain {NAME} deleted", exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_contact_list(self, cli, credentials, exc):
        """Test contact list command."""
        with patch("dnsgateway.cli.DnsGatewayClient.contacts",
                   new_callable=PropertyMock) as m:
            m.return_value = CONTACTS
            m.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "contact", "list"))
            m.assert_called_once_with()
        assert self._check_result(CONTACT, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_contact_show(self, cli, credentials, exc):
        """Test contact show command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            client.contact.return_value = CONTACT
            client.contact.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "contact", "show", CONTACT_ID))
            client.contact.assert_called_once_with(id=CONTACT_ID)
        assert self._check_result(CONTACT, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_contact_create(self, cli, credentials, exc):
        """Test contact create command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            client.create_contact.return_value = CONTACT
            client.create_contact.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "contact", "create",
                                       "--id", CONTACT_ID,
                                       "--name", "Test Contact",
                                       "--email", "test@example.com",
                                       "--phone", "+27.110001111",
                                       "--city", "Test City",
                                       "--country", "ZA"))
            client.create_contact.assert_called_once_with(id=CONTACT_ID,
                                                          name="Test Contact",
                                                          org=None,
                                                          email="test@example.com",  # noqa: E501
                                                          phone="+27.110001111",  # noqa: E501
                                                          fax=None,
                                                          address1=None,
                                                          address2=None,
                                                          address3=None,
                                                          city="Test City",
                                                          province=None,
                                                          code=None,
                                                          country="ZA")
        assert self._check_result(CONTACT, exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_contact_delete(self, cli, credentials, exc):
        """Test contact delete command."""
        with patch("dnsgateway.cli.DnsGatewayClient", autospec=True) as m:
            client = m.return_value
            contact = client.contact.return_value
            contact.delete.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "contact", "delete", CONTACT_ID))  # noqa: E501
            client.contact.assert_called_once_with(id=CONTACT_ID)
            contact.delete.assert_called_once_with()
        assert self._check_result(f"Contact {CONTACT_ID} deleted", exc, result)

    @pytest.mark.parametrize("exc", ((DEFAULT,), Exception))
    def test_zone_list(self, cli, credentials, exc):
        """Test zone list command."""
        with patch("dnsgateway.cli.DnsGatewayClient.zones",
                   new_callable=PropertyMock) as m:
            m.return_value = ZONES
            m.side_effect = exc
            result = cli.invoke(main, ("-u", credentials["username"],
                                       "-p", credentials["password"],
                                       "--dev", "zone", "list"))
            m.assert_called_once_with()
        assert self._check_result(ZONE, exc, result)
