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

from dnsgateway.__meta__ import __version__ as version
from dnsgateway.cli import main


class TestCli(object):
    """Test cases for cli tool."""

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
