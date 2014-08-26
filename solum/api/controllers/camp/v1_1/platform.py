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

from solum.api.controllers.camp.v1_1.datamodel import platform as model

from solum.common import exception


description_string = "Solum CAMP API platform resource for CAMP v1.1."


class Controller():
    """platform controller"""

    @exception.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(model.Platform)
    def index(self):
        return model.Platform(uri=pecan.request.host_url +
                               '/camp/v1_1/platform/',
                              name='Solum_CAMP_v1_1_platform',
                              type='platform',
                              description=description_string,
                              supported_formats_uri=pecan.request.host_url +
                               '/camp/v1_1/formats/',
                              extensions_uri=pecan.request.host_url +
                               '/camp/v1_1/extensions/',
                              type_definitions_uri=pecan.request.host_url +
                               '/camp/v1_1/type_definitions/',
                              platform_endpoints_uri=pecan.request.host_url +
                               '/camp/platform_endpoints/',
                              specification_version='CAMP 1.1',
                              implementation_version='Solum CAMP 1.1',
                              assemblies_uri=pecan.request.host_url +
                               '/camp/v1_1/assemblies/',
                              services_uri=pecan.request.host_url +
                               '/camp/v1_1/services/',
                              plans_uri=pecan.request.host_url +
                               '/camp/v1_1/plans/')
