# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlalchemy

from solum.common import exception
from solum.objects import extension as abstract
from solum.objects.sqlalchemy import models as sql
from solum.openstack.common.db.sqlalchemy import session as db_session


class Extension(sql.Base, abstract.Extension):
    """Represent an extension in sqlalchemy."""

    __resource__ = 'extensions'
    __tablename__ = 'extension'
    __table_args__ = sql.table_args()

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    uuid = sqlalchemy.Column(sqlalchemy.String(36))
    project_id = sqlalchemy.Column(sqlalchemy.String(36))
    user_id = sqlalchemy.Column(sqlalchemy.String(36))
    description = sqlalchemy.Column(sqlalchemy.String(255))
    name = sqlalchemy.Column(sqlalchemy.String(100))
    version = sqlalchemy.Column(sqlalchemy.String(16))
    documentation = sqlalchemy.Column(sqlalchemy.String(255))

    @classmethod
    def _raise_duplicate_object(cls, e, self):
        raise exception.ExtensionExists()

    @classmethod
    def get_by_uuid(cls, context, item_uuid):
        try:
            return db_session.get_session().query(cls).filter_by(
                uuid=item_uuid).one()
        except sqlalchemy.orm.exc.NoResultFound:
            cls._raise_not_found(item_uuid)


class ExtensionList(abstract.ExtensionList):
    """Represent a list of extensions in sqlalchemy."""

    @classmethod
    def get_all(cls, context):
        return ExtensionList(sql.model_query(context, Extension))
