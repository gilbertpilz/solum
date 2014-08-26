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

import copy

from wsme import types as wtypes

from solum.api.controllers import common_types
from solum.api.controllers.v1.datamodel import types as api_types

#from solum.openstack.common import log as logging


#LOG = logging.getLogger(__name__)


class ParameterDefinitionLink(common_types.Link):
    """ParameterLink attribute type"""

    required = bool
    """Indicates whether the parameter referenced by this Link is required."""

    default_value = wtypes.Base
    """Default value for the parameter referenced by this Link."""


class ParameterDefinitions(api_types.Base):
    """parameter_definitions resource"""

    parameter_definition_links = [ParameterDefinitionLink]
    """The value of the parameter_definition_links attribute is an array of
     extended Link elements that reference parameter_definition resources."""

    def __init__(self, **kwds):
#        LOG.debug("ParameterDefinitions constructor: %s" % kwds)
        super(ParameterDefinitions, self).__init__(**kwds)

    def fix_uris(self, host_url):
        """Update the URIs in a parameter_definitions resource to reflect
         the URL of the current host."""
        ret_val = copy.deepcopy(self)
        ret_val.uri = '%s/camp/v1_1/parameter_definitions/%s' % (host_url,
                                                                 ret_val.uri)
        for pd_link in ret_val.parameter_definition_links:
            pd_link.href = '%s/camp/v1_1/param_def/%s' % (host_url,
                                                          pd_link.href)
        return ret_val
