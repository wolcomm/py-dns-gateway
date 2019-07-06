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

    base_path = "registry"

    _keys = ()

    _properties = {}

    def __init__(self, client=None, **kwargs):
        """Initialise a new instance."""
        self.client = client
        self._update_properties(**kwargs)

    def _update_properties(self, **kwargs):
        """Replace the internal attr dictionary with kwargs."""
        self._properties = {k: v for k, v in kwargs.items() if k in self._keys}

    def __getattr__(self, name):
        """Return value from internal attribute dictionary."""
        try:
            return self._properties[name]
        except KeyError as e:
            log.error(e)
            raise AttributeError(e)

    def __setattr__(self, name, value):
        """Set the requested value on the internal attr dictionary."""
        if name in self._keys:
            self.update(**{name: value})
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        """Serialise object to json."""
        return json.dumps(self._properties, indent=4)

    @property
    def path(self):
        """Get the URI path to the instance."""
        return f"{self.base_path}/{self.wid}"

    def refresh(self):
        """Refresh the object properties."""
        props = self.client.get(path=self.path)
        self._update_properties(**props)
        return self

    def update(self, **kwargs):
        """Update the object."""
        data = {k: v for k, v in kwargs.items() if k in self._keys}
        props = self.client.put(path=self.path, data=data)
        self._update_properties(**props)
        return self
