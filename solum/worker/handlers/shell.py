# Copyright 2014 - Rackspace Hosting
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Solum Worker shell handler."""

import os
import subprocess

import solum
from solum.common import exception
from solum.common import solum_keystoneclient
from solum.conductor import api as conductor_api
from solum.deployer import api as deployer_api
from solum.objects import assembly
from solum.objects import image
from solum.openstack.common import log as logging
from solum.openstack.common import uuidutils

LOG = logging.getLogger(__name__)

ASSEMBLY_STATES = assembly.States
IMAGE_STATES = image.States


def job_update_notification(ctxt, build_id, state=None, description=None,
                            created_image_id=None, assembly_id=None):
    """send a status update to the conductor."""
    LOG.debug('build id:%s %s (%s) %s %s' % (build_id, state, description,
                                             created_image_id, assembly_id),
              context=solum.TLS.trace)
    conductor_api.API(context=ctxt).build_job_update(build_id, state,
                                                     description,
                                                     created_image_id,
                                                     assembly_id)


def update_assembly_status(ctxt, assembly_id, status):
    # TODO(datsun180b): use conductor to update assembly status
    if assembly_id is None:
        return
    assem = solum.objects.registry.Assembly.get_by_id(ctxt,
                                                      assembly_id)
    assem.status = status
    assem.save(ctxt)


class Handler(object):
    def echo(self, ctxt, message):
        LOG.debug("%s" % message)

    @exception.wrap_keystone_exception
    def _get_environment(self, ctxt):
        kc = solum_keystoneclient.KeystoneClientV3(ctxt)
        image_url = kc.client.service_catalog.url_for(
            service_type='image',
            endpoint_type='publicURL')

        # create a minimal environment
        user_env = {}
        for var in ['PATH', 'LOGNAME', 'LANG', 'HOME', 'USER', 'TERM']:
            if var in os.environ:
                user_env[var] = os.environ[var]
        user_env['OS_AUTH_TOKEN'] = ctxt.auth_token
        user_env['OS_AUTH_URL'] = ctxt.auth_url
        user_env['OS_IMAGE_URL'] = image_url
        return user_env

    @property
    def proj_dir(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', '..', '..'))

    def _get_build_command(self, ctxt, source_uri, name, base_image_id,
                           source_format, image_format):
        # map the input formats to script paths.
        # TODO(asalkeld) we need an "auto".
        pathm = {'heroku': 'lp-cedarish',
                 'dib': 'diskimage-builder',
                 'dockerfile': 'lp-dockerfile',
                 'docker': 'docker',
                 'qcow2': 'vm-slug'}
        if base_image_id == 'auto' and image_format == 'qcow2':
            base_image_id = 'cedarish'
        build_app = os.path.join(self.proj_dir, 'contrib',
                                 pathm.get(source_format, 'lp-cedarish'),
                                 pathm.get(image_format, 'vm-slug'),
                                 'build-app')
        return [build_app, source_uri, name, ctxt.tenant, base_image_id]

    def build(self, ctxt, build_id, source_uri, name, base_image_id,
              source_format, image_format, assembly_id, test_cmd):

        # TODO(datsun180b): This is only temporary, until Mistral becomes our
        # workflow engine.
        if self._run_unittest(ctxt, assembly_id, source_uri, test_cmd) != 0:
            return

        update_assembly_status(ctxt, assembly_id, ASSEMBLY_STATES.BUILDING)

        solum.TLS.trace.clear()
        solum.TLS.trace.import_context(ctxt)

        build_cmd = self._get_build_command(ctxt, source_uri, name,
                                            base_image_id,
                                            source_format, image_format)
        solum.TLS.trace.support_info(build_cmd=' '.join(build_cmd),
                                     assembly_id=assembly_id)

        try:
            user_env = self._get_environment(ctxt)
        except exception.SolumException as env_ex:
            LOG.exception(env_ex)
            job_update_notification(ctxt, build_id, IMAGE_STATES.ERROR,
                                    description=str(env_ex),
                                    assembly_id=assembly_id)
            return

        log_env = user_env.copy()
        if 'OS_AUTH_TOKEN' in log_env:
            del log_env['OS_AUTH_TOKEN']
        solum.TLS.trace.support_info(environment=log_env)

        job_update_notification(ctxt, build_id, IMAGE_STATES.BUILDING,
                                description='Starting the image build',
                                assembly_id=assembly_id)
        try:
            out = subprocess.Popen(build_cmd,
                                   env=user_env,
                                   stdout=subprocess.PIPE).communicate()[0]
        except OSError as subex:
            LOG.exception(subex)
            job_update_notification(ctxt, build_id, IMAGE_STATES.ERROR,
                                    description=subex, assembly_id=assembly_id)
            return
        # we expect one line in the output that looks like:
        # created_image_id=<the glance_id>
        created_image_id = None
        for line in out.split('\n'):
            if 'created_image_id' in line:
                solum.TLS.trace.support_info(build_out_line=line)
                created_image_id = line.split('=')[-1].strip()
        if not uuidutils.is_uuid_like(created_image_id):
            job_update_notification(ctxt, build_id, IMAGE_STATES.ERROR,
                                    description='image not created',
                                    assembly_id=assembly_id)
            return
        job_update_notification(ctxt, build_id, IMAGE_STATES.COMPLETE,
                                description='built successfully',
                                created_image_id=created_image_id,
                                assembly_id=assembly_id)
        if assembly_id is not None:
            deployer_api.API(context=ctxt).deploy(assembly_id=assembly_id,
                                                  image_id=created_image_id)

    def _run_unittest(self, ctxt, assembly_id, git_url, test_cmd):
        if test_cmd is None:
            LOG.debug("Unit test command is None; skipping unittests.")
            return 0

        git_branch = 'master'

        LOG.debug("Running unittests.")
        update_assembly_status(ctxt, assembly_id, ASSEMBLY_STATES.UNIT_TESTING)

        test_app = os.path.join(self.proj_dir, 'contrib', 'lp-cedarish',
                                'docker', 'unittest-app')
        command = [test_app, git_url, git_branch, ctxt.tenant, test_cmd]

        solum.TLS.trace.clear()
        solum.TLS.trace.import_context(ctxt)

        user_env = self._get_environment(ctxt)
        log_env = user_env.copy()
        if 'OS_AUTH_TOKEN' in log_env:
            del log_env['OS_AUTH_TOKEN']
        solum.TLS.trace.support_info(environment=log_env)

        returncode = -1
        try:
            runtest = subprocess.Popen(command, env=user_env)
            returncode = runtest.wait()
        except OSError as subex:
            LOG.exception("Exception running unit tests:")
            LOG.exception(subex)

        if returncode != 0:
            LOG.error("Unit tests failed. Return code is %r" % (returncode))
            update_assembly_status(ctxt, assembly_id,
                                   ASSEMBLY_STATES.UNIT_TESTING_FAILED)

        return returncode

    def unittest(self, ctxt, assembly_id, git_url, test_cmd):
        self._run_unittest(ctxt, assembly_id, git_url, test_cmd)
