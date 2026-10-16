"""
Unit tests for suite-api-network cURL parser business logic.
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.curl_parser import parse_curl_to_python


class TestCurlParser(unittest.TestCase):
    def test_simple_get(self):
        res = parse_curl_to_python("curl https://api.developeros.in/v1/tools")
        self.assertEqual(res["method"], "GET")
        self.assertEqual(res["url"], "https://api.developeros.in/v1/tools")
        self.assertIn('requests.get("https://api.developeros.in/v1/tools")', res["python_code"])

    def test_post_with_headers_and_json(self):
        cmd = """
        curl -X POST https://api.developeros.in/v1/convert \\
          -H "Content-Type: application/json" \\
          -H "Authorization: Bearer test_token" \\
          -d '{"name": "DeveloperOS", "active": true}'
        """
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["method"], "POST")
        self.assertEqual(res["url"], "https://api.developeros.in/v1/convert")
        self.assertEqual(res["headers"]["Content-Type"], "application/json")
        self.assertEqual(res["headers"]["Authorization"], "Bearer test_token")
        self.assertIn("DeveloperOS", res["data"])
        self.assertIn("requests.post", res["python_code"])
        self.assertIn("fetch", res["js_code"])

    def test_empty_input(self):
        res = parse_curl_to_python("")
        self.assertEqual(res["url"], "")
        self.assertEqual(res["method"], "GET")
        self.assertIn("Please provide a valid cURL command", res["python_code"])

    def test_basic_auth(self):
        cmd = "curl -u admin:secret123 https://api.developeros.in/admin"
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["auth"], ("admin", "secret123"))
        self.assertIn("auth = ('admin', 'secret123')", res["python_code"])
        self.assertIn("Basic", res["js_code"])

    def test_user_agent_and_cookie(self):
        cmd = 'curl -A "CustomBot/1.0" -b "session_id=xyz987" https://developeros.in'
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["headers"]["User-Agent"], "CustomBot/1.0")
        self.assertEqual(res["headers"]["Cookie"], "session_id=xyz987")

    def test_custom_http_method(self):
        cmd = "curl -X DELETE https://api.developeros.in/item/42"
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["method"], "DELETE")
        self.assertIn("requests.delete", res["python_code"])

    def test_data_binary_infers_post(self):
        cmd = "curl --data-binary @payload.json https://api.developeros.in/upload"
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["method"], "POST")
        self.assertEqual(res["data"], "@payload.json")


if __name__ == "__main__":
    unittest.main()
