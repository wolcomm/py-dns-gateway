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
"""dnsgateway.zone module."""

import logging

from dnsgateway.base import BaseObject

log = logging.getLogger(__name__)


class Zone(BaseObject):
    """Zone object implementation."""

    _attrs = {
        "wid": lambda v: isinstance(v, int),
        "cdate": lambda v: v,
        "operator": lambda v: v,
        "url": lambda v: v,
        "zone": lambda v: v,
        "default_allow": lambda v: isinstance(v, bool),
        "zone_access": lambda v: v,
        "transport": lambda v: v,
        "passthrough": lambda v: isinstance(v, bool),
    }
