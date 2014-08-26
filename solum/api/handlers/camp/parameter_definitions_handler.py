# Copyright 2013 - Rackspace
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


from solum.api.controllers.camp.v1_1.datamodel import \
    parameter_definitions as pd
from solum.api.handlers import handler

from solum.openstack.common import log as logging

LOG = logging.getLogger(__name__)

ASSEMB_PARAM_DESCRIPTION = "Solum CAMP API definitions of the 'pdp_uri',\
 'plan_uri', 'pdp_file', and 'plan_file' parameters."

ASSEMB_PARAM_LINKS = [
    pd.ParameterDefinitionLink(href='pdp_uri_param',
                               target_name='Solum_CAMP_PDP_URI_Parameter',
                               required=False),
    pd.ParameterDefinitionLink(href='plan_uri_param',
                               target_name='Solum_CAMP_Plan_URI_Parameter',
                               required=False),
    pd.ParameterDefinitionLink(href='pdp_file_param',
                               target_name="Solum_CAMP_PDP_File_Parameter",
                               required=False),
    pd.ParameterDefinitionLink(href='plan_file_param',
                               target_name="Solum_CAMP_Plan_File_Parameter",
                               required=False)
]

NDT_PARAM_DESCRIPTION = "Solum CAMP API definitions of the 'name',\
 'description', and 'tag' parameters."

NDT_PARAM_LINKS = [
    pd.ParameterDefinitionLink(href='name_param',
                               target_name='Solum_CAMP_Name_Parameter',
                               required=False),
    pd.ParameterDefinitionLink(href='description_param',
                               target_name='Solum_CAMP_Definition_Parameter',
                               required=False),
    pd.ParameterDefinitionLink(href='tags_param',
                               target_name='Solum_CAMP_Tags_Parameter',
                               required=False)
]

GLOBAL_PARAM_DEFS = {
    'assembly_create_params':
        pd.ParameterDefinitions(uri='assembly_create_params',
                                name='Solum_CAMP_assembly_create_parameters',
                                type='parameter_definitions',
                                description=ASSEMB_PARAM_DESCRIPTION,
                                parameter_definition_links=ASSEMB_PARAM_LINKS),
    'ndt_params':
        pd.ParameterDefinitions(uri='ndt_params',
                                name='Solum_CAMP_NDT_parameters',
                                type='parameter_definitions',
                                description=NDT_PARAM_DESCRIPTION,
                                parameter_definition_links=NDT_PARAM_LINKS)
}


class ParameterDefinitionsHandler(handler.Handler):

    def get(self, path):
        if path in GLOBAL_PARAM_DEFS:
            return GLOBAL_PARAM_DEFS[path]
