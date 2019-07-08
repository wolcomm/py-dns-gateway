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
"""dnsgateway.helpers module."""

import logging
import secrets
import string

log = logging.getLogger(__name__)


def gen_authinfo(name, length=16):
    """Generate an authinfo code appropriate to the domain name."""
    log.debug(f"Generating authinfo for domain {name}")
    if name.endswith(".co.za"):
        authinfo = "coza"
    else:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            authinfo = "".join(secrets.choice(alphabet) for i in range(length))
            if (any(char.isalpha() for char in authinfo)
                    and any(char.isdigit() for char in authinfo)
                    and any(char in string.punctuation for char in authinfo)):
                break
    return authinfo
