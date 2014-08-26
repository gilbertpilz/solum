# -*- coding: utf-8 -*-
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

import mock

from solum import objects
from solum.tests import base
from solum.tests import fakes

from solum.api.controllers.camp.v1_1 import services


@mock.patch('pecan.request', new_callable=fakes.FakePecanRequest)
@mock.patch('pecan.response', new_callable=fakes.FakePecanResponse)
class TestServices(base.BaseTestCase):
    def setUp(self):
        super(TestServices, self).setUp()
        objects.load()

    def test_services_get(self, resp_mock, request_mock):
        fake_services = fakes.FakeCAMPServices()
        cont = services.Controller()
        resp = cont.index()
        self.assertEqual(200, resp_mock.status)
        self.assertEqual(fake_services.name, resp['result'].name)
        self.assertEqual(fake_services.type, resp['result'].type)
