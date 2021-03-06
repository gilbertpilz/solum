# Copyright 2014 - Rackspace
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

from solum.api.handlers import language_pack_handler
from solum.tests import base
from solum.tests import utils

image_sample = {"status": "active",
                "name": "nodeus",
                "tags": [
                    "solum::lp",
                    "solum::lp::name::fake_name",
                    "solum::lp::type::fake_type",
                    "solum::lp::compiler_version::1.3",
                    "solum::lp::compiler_version::1.4",
                    "solum::lp::compiler_version::1.5",
                    "solum::lp::runtime_version::1.4",
                    "solum::lp::runtime_version::1.5",
                    "solum::lp::runtime_version::1.6",
                    "solum::lp::implementation::Sun",
                    "solum::lp::build_tool::maven::3.0",
                    "solum::lp::build_tool::ant::2.1",
                    "solum::lp::os_platform::Ubuntu::12.04",
                    "solum::lp::attribute::attr1key::attr1value",
                    "solum::lp::attribute::attr2key::attr2value"
                ],
                "self": "/v2/images/bc68cd73",
                "id": "bc68cd73"}


@mock.patch('solum.common.clients.OpenStackClients')
class TestLanguagePackHandler(base.BaseTestCase):
    def setUp(self):
        super(TestLanguagePackHandler, self).setUp()
        self.ctx = utils.dummy_context()

    def test_language_pack_get(self, mock_clients):
        images_get = mock_clients.return_value.glance.return_value.images.get
        images_get.return_value = image_sample
        handler = language_pack_handler.LanguagePackHandler(self.ctx)
        resp = handler.get('test_id')
        self.assertIsNotNone(resp)
        images_get.assert_called_once_with('test_id')

    def test_language_pack_get_all(self, mock_clients):
        images_list = mock_clients.return_value.glance.return_value.images.list
        images_list.return_value = [image_sample]
        handler = language_pack_handler.LanguagePackHandler(self.ctx)
        resp = handler.get_all()
        self.assertIsNotNone(resp)
        images_list.assert_called_once_with(filters={'tag': ['solum::lp']})

    def test_create(self, mock_clients):
        data = {'name': 'new_name'}
        img_mock = mock_clients.return_value.glance.return_value.images.create
        img_mock.return_value = image_sample
        handler = language_pack_handler.LanguagePackHandler(self.ctx)
        res = handler.create(data)
        img_mock.assert_called_once_with(**data)
        self.assertEqual(res, image_sample)

    def test_update(self, mock_clients):
        data = {'name': 'new_name'}
        img_mock = mock_clients.return_value.glance.return_value.images.update
        img_mock.return_value = image_sample
        handler = language_pack_handler.LanguagePackHandler(self.ctx)
        res = handler.update('fake_id', data)
        img_mock.assert_called_once_with('fake_id', **data)
        self.assertEqual(res, image_sample)

    def test_delete(self, mock_clients):
        img_mock = mock_clients.return_value.glance.return_value.images.delete
        handler = language_pack_handler.LanguagePackHandler(self.ctx)
        handler.delete('test_id')
        img_mock.assert_called_once_with('test_id')
