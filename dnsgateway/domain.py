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

    base_path = f"{BaseObject.base_path}/domains"

    _keys = ("wid", "name", "zone", "zone_id", "transport", "passthrough",
             "registrant", "admin", "tech", "billing", "cdate", "expiry",
             "curExpDate", "rar", "period", "period_unit", "autorenew",
             "authinfo", "detail", "hosts", "contacts", "statuses", "events",
             "domainsec", "rgp_statuses", "fee_commands", "charge")
