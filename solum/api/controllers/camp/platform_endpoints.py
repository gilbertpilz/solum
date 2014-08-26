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

import pecan

import wsmeext.pecan as wsme_pecan

from solum.api.controllers import common_types
from solum.api.controllers.camp.datamodel import platform_endpoints as model

from solum.common import exception


description_string = "Solum CAMP API platform_endpoints resource."


class Controller(object):
    """platform_endpoints controller"""

    @exception.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(model.PlatformEndpoints)
    def index(self):
        links = [
            common_types.Link(href=pecan.request.host_url +
                               '/camp/camp_v1_1_endpoint/',
                              target_name='Solum_CAMP_1_1_endpoint')
        ]

        return model.PlatformEndpoints(uri=pecan.request.host_url +
                                        '/camp/platform_endpoints/',
                                       name='Solum_CAMP_endpoints',
                                       type='platform_endpoints',
                                       description=description_string,
                                       platform_endpoint_links=links)
