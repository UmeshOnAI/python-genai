# Copyright 2024 Google LLC
#
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
#


"""Tests for models.get."""

import pytest
from ... import errors
from ... import types
from .. import pytest_helper

test_table: list[pytest_helper.TestTableItem] = [
    pytest_helper.TestTableItem(
        name='test_get_vertex_tuned_model',
        parameters=types._GetModelParameters(model='models/7687416965014487040'),
        exception_if_mldev='404',
    ),
    pytest_helper.TestTableItem(
        name='test_get_mldev_tuned_model',
        parameters=types._GetModelParameters(
            model='tunedModels/generate-num-1896'
        ),
        exception_if_vertex='404',
    ),
    pytest_helper.TestTableItem(
        name='test_get_base_model',
        parameters=types._GetModelParameters(model='gemini-1.5-flash'),
        # TODO(b/382104121): Add test for base model once Vertex support it.
        exception_if_vertex='404',
    ),
    pytest_helper.TestTableItem(
        name='test_get_base_model_with_models_prefix',
        parameters=types._GetModelParameters(model='models/gemini-1.5-flash'),
        exception_if_vertex='400',
    ),
]
pytestmark = pytest_helper.setup(
    file=__file__,
    globals_for_file=globals(),
    test_method='models.get',
    test_table=test_table,
)


@pytest.mark.asyncio
async def test_async_get_tuned_model(client):
  if client._api_client.vertexai:
    with pytest.raises(errors.ClientError) as e:
      await client.aio.models.get(model='tunedModels/generate-num-1896')
      assert '404' in str(e)
  else:
    response = await client.aio.models.get(
        model='tunedModels/generate-num-1896'
    )


@pytest.mark.asyncio
async def test_async_get_model(client):
  if client._api_client.vertexai:
    response = await client.aio.models.get(model='models/7687416965014487040')
  else:
    with pytest.raises(errors.ClientError) as e:
      await client.aio.models.get(model='models/7687416965014487040')
      assert '404' in str(e)