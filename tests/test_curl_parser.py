"""
Unit tests for suite-api-network business logic.
"""

import sys
import unittest
from pathlib import Path

# Ensure suite root is in sys.path
SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.curl_parser import parse_curl_to_python


class TestCurlParser(unittest.TestCase):
    def test_parse_simple_get(self):
        res = parse_curl_to_python('curl "https://api.developeros.in/health"')
        self.assertEqual(res["url"], "https://api.developeros.in/health")
        self.assertEqual(res["method"], "GET")
        self.assertIn("requests.get", res["python_code"])

    def test_parse_post_with_headers_and_body(self):
        cmd = 'curl -X POST "https://api.developeros.in/v1/auth" -H "Content-Type: application/json" -d \'{"key":"value"}\''
        res = parse_curl_to_python(cmd)
        self.assertEqual(res["method"], "POST")
        self.assertEqual(res["headers"].get("Content-Type"), "application/json")
        self.assertIn("requests.post", res["python_code"])
        self.assertIn("fetch", res["js_code"])


if __name__ == "__main__":
    unittest.main()
