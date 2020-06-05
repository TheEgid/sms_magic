import unittest
from jsonschema import validate
from main import request_smsc
from unittest.mock import patch, Mock, AsyncMock
import pytest
import json


# class TestGetData:
#
#     def setUp(self):
#         self.valid_schema = {
#             "type": "object",
#             "id": {"type": "number"},
#             "cnt": {"type": "number"},
#             "required": ["id", "cnt"]
#         }
#
#     @pytest.mark.asyncio
#     @patch('main.test_get_post')
#     async def test_get_post(self, mock_make_request):
#         mock_status_200 = Mock(status_code=200)
#         mock_status_200.json.return_value = {
#             "id": 100,
#             "cnt": 1
#         }
#         mock_make_request.return_value = mock_status_200
#
#         payload = {'phones': 88007003300, 'mes': 'test_msg'}
#         result = await request_smsc('send', 'test_user', 'test_password', payload)
#         #result = json.loads(result)
#         #assert isinstance(result, dict)
#         #validate(resp, self.valid_schema)
#         # self.assertIsInstance(resp, dict)
#         # self.assertTrue(resp)
#         # self.assertEqual(resp["body"], body)


@pytest.mark.asyncio
@patch('main.request_smsc')
async def test_main_function(request_smsc):
    mock_status_200 = AsyncMock(status_code=200)
    mock_status_200.json.return_value = {
                "id": 100,
                "cnt": 1
            }


if __name__ == '__main__':
    pytest.main([__file__, '--capture=sys', '--tb=line', '-v'])




    #mock_function.assert_called_once_with(1, 2, 3)
