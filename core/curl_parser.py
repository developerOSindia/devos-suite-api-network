"""
Pure business logic for cURL command parsing and code generation.
Zero Streamlit or UI dependencies.
"""

import shlex
import re
from typing import Dict, Any


def parse_curl_to_python(curl_command: str) -> Dict[str, Any]:
    """Parses a raw cURL command into equivalent Python requests and JavaScript fetch code."""
    curl_clean = curl_command.strip()
    if not curl_clean:
        return {
            "url": "",
            "method": "GET",
            "headers": {},
            "data": "",
            "python_code": "# Please provide a valid cURL command",
            "js_code": "// Please provide a valid cURL command"
        }

    # Normalize line breaks and backslashes
    cmd = curl_clean.replace("\\\n", " ").replace("\\\r\n", " ").strip()
    
    try:
        tokens = shlex.split(cmd)
    except Exception:
        tokens = cmd.split()

    method = "GET"
    url = ""
    headers = {}
    data = ""

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ("-X", "--request") and i + 1 < len(tokens):
            method = tokens[i + 1].upper()
            i += 2
        elif token in ("-H", "--header") and i + 1 < len(tokens):
            header_val = tokens[i + 1]
            if ":" in header_val:
                k, v = header_val.split(":", 1)
                headers[k.strip()] = v.strip()
            i += 2
        elif token in ("-d", "--data", "--data-raw") and i + 1 < len(tokens):
            data = tokens[i + 1]
            if method == "GET":
                method = "POST"
            i += 2
        elif token.startswith("http://") or token.startswith("https://"):
            url = token
            i += 1
        elif token not in ("curl",) and not url and not token.startswith("-"):
            url = token
            i += 1
        else:
            i += 1

    # Python Requests Code
    py_lines = ["import requests", ""]
    if headers:
        py_lines.append(f"headers = {repr(headers)}")
    if data:
        py_lines.append(f"data = {repr(data)}")
    
    req_args = [f'"{url}"']
    if headers:
        req_args.append("headers=headers")
    if data:
        req_args.append("data=data")

    py_lines.append(f"response = requests.{method.lower()}({', '.join(req_args)})")
    py_lines.append("print(response.status_code)")
    py_lines.append("print(response.text)")

    # JavaScript Fetch Code
    js_opts = [f'  method: "{method}"']
    if headers:
        js_opts.append(f'  headers: {json_repr(headers)}')
    if data:
        js_opts.append(f'  body: JSON.stringify({repr(data)})')

    js_lines = [
        f'fetch("{url}", {{',
        ",\n".join(js_opts),
        "})",
        "  .then(res => res.json())",
        "  .then(data => console.log(data))",
        "  .catch(err => console.error(err));"
    ]

    return {
        "url": url,
        "method": method,
        "headers": headers,
        "data": data,
        "python_code": "\n".join(py_lines),
        "js_code": "\n".join(js_lines)
    }


def json_repr(d: dict) -> str:
    import json
    return json.dumps(d, indent=4)
