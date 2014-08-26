#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from solum.api.controllers import common_types
from solum.api.controllers.v1.datamodel import types as api_types

#from solum.openstack.common import log as logging


#LOG = logging.getLogger(__name__)


class TypeDefinitions(api_types.Base):
    """type_definitions resource"""

    type_definition_links = [common_types.Link]
    """This attribute contains Links to type_definition resources that contain
     information about resource types supported by the Platform."""

    def __init__(self, **kwds):
#        LOG.debug("type_definitions constructor: %s" % kwds)
        super(TypeDefinitions, self).__init__(**kwds)
