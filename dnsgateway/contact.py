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
"""dnsgateway.contact module."""

import logging

from dnsgateway.base import BaseObject

log = logging.getLogger(__name__)


class Contact(BaseObject):
    """Contact object implementation."""

    _attrs = {
        "wid": lambda v: isinstance(v, int),
        "id": lambda v: v,
        "cdate": lambda v: v,
        "name": lambda v: v,
        "phone": lambda v: v,
        "fax": lambda v: v,
        "email": lambda v: v,
        "contact_address": lambda v: isinstance(v, list),
        "statuses": lambda v: v,
        "linked": lambda v: isinstance(v, bool),
        "detail": lambda v: v,
        "domains": lambda v: isinstance(v, int)
    }
