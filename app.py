"""
DeveloperOS API & Network Suite - Interactive Application
"""

import streamlit as st
from core.curl_parser import parse_curl_to_python
from ui.components import render_suite_header, render_suite_footer, render_main_promotional_banner

st.set_page_config(
    page_title="DeveloperOS - API & Network Suite",
    page_icon="🔌",
    layout="wide",
)


def main():
    render_suite_header(
        title="cURL to Python / JavaScript Converter",
        description="Convert raw cURL shell commands into idiomatic Python requests and JavaScript fetch code instantly.",
    )

    sample_curl = 'curl -X POST "https://api.developeros.in/v1/auth" \\\n  -H "Content-Type: application/json" \\\n  -H "Authorization: Bearer devos_demo_token" \\\n  -d \'{"service": "metrics", "enabled": true}\''

    curl_input = st.text_area("Paste Raw cURL Command:", value=sample_curl, height=130)

    if curl_input:
        parsed = parse_curl_to_python(curl_input)

        col_py, col_js = st.columns(2, gap="large")

        with col_py:
            st.subheader("Python (requests)")
            st.code(parsed["python_code"], language="python")

        with col_js:
            st.subheader("JavaScript (fetch)")
            st.code(parsed["js_code"], language="javascript")

    render_main_promotional_banner()
    render_suite_footer()


if __name__ == "__main__":
    main()
