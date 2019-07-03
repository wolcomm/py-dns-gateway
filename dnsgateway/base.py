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

import json
import logging

log = logging.getLogger(__name__)


class BaseObject(object):
    """Base object implementation."""

    _attrs = {}

    _dict = {}

    def __init__(self, client=None, **kwargs):
        """Initialise a new instance."""
        self.client = client
        self._update_dict(**kwargs)

    def _update_dict(self, **kwargs):
        """Replace the internal attr dictionary with kwargs."""
        self._dict = {k: self._validate(k, v) for k, v in kwargs.items()}

    def _validate(self, key, value):
        """Validate the value provided for 'key'."""
        try:
            valid = self._attrs[key](value)
        except KeyError as e:
            log.error(e)
            raise AttributeError(e)
        except Exception as e:
            log.error(e)
            raise ValueError(e)
        if not valid:
            msg = f"Invalid value for {key}: {value}"
            e = ValueError(msg)
            log.error(e)
            raise e
        return value

    def __getattr__(self, name):
        """Return value from internal attribute dictionary."""
        try:
            return self._dict[name]
        except KeyError as e:
            log.error(e)
            raise AttributeError(e)

    def update(self, **kwargs):
        """Update the object."""
        data = {k: self._validate(k, v) for k, v in kwargs.items()}
        resp = self.client.put(path=self.path, data=data)
        self._update_dict(**resp)

    def __setattr__(self, name, value):
        """Set the requested value on the internal attr dictionary."""
        if name in self._attrs:
            self.update(**{name: value})
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        """Serialise object to json."""
        return json.dumps(self._dict, indent=4)
