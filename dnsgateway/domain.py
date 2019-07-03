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
"""dnsgateway.domain module."""

import logging

from dnsgateway.base import BaseObject

log = logging.getLogger(__name__)


class Domain(BaseObject):
    """Domain object implementation."""

    _attrs = {
        "wid": lambda v: isinstance(v, int),
        "name": lambda v: v,
        "zone": lambda v: v,
        "zone_id": lambda v: v,
        "transport": lambda v: v,
        "passthrough": lambda v: isinstance(v, bool),
        "registrant": lambda v: v,
        "admin": lambda v: v,
        "tech": lambda v: v,
        "billing": lambda v: v,
        "cdate": lambda v: v,
        "expiry": lambda v: v,
        "curExpDate": lambda v: v,
        "rar": lambda v: v,
        "period": lambda v: v,
        "period_unit": lambda v: v,
        "autorenew": lambda v: isinstance(v, bool),
        "authinfo": lambda v: v,
        "detail": lambda v: v,
        "hosts": lambda v: v,
        "contacts": lambda v: v,
        "statuses": lambda v: v,
        "events": lambda v: v,
        "domainsec": lambda v: v,
        "rgp_statuses": lambda v: v,
        "fee_commands": lambda v: v,
        "charge": lambda v: v,
    }
