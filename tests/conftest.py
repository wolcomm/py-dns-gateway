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

from dnsgateway import DnsGatewayClient
from dnsgateway.client import DEVELOPMENT_ENDPOINT

import pytest


@pytest.fixture()
def client():
    """Get an instance of DnsGatewayClient as a test fixture."""
    credentials_path = os.path.join(os.path.dirname(__file__),
                                    "credentials.json.secret")
    with open(credentials_path) as f:
        credentials = json.load(f)
    api_client = DnsGatewayClient(endpoint=DEVELOPMENT_ENDPOINT, **credentials)
    return api_client