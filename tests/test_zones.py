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
"""dnsgateway client zone management tests."""

from dnsgateway import DnsGatewayClient
from dnsgateway.zone import Zone


class TestZones(object):
    """Test cases for zone management."""

    def test_instance(self, client):
        """Test instantiation."""
        assert isinstance(client, DnsGatewayClient)

    def test_zones(self, client):
        """Test zones property."""
        for zone in client.zones:
            assert isinstance(zone, Zone)
