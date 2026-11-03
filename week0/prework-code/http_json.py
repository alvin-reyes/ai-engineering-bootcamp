"""Builder prework: call a JSON API (PyPI package info) with the standard library, with a timeout and error handling."""
import json
import sys
import urllib.error
import urllib.request

package = sys.argv[1] if len(sys.argv) > 1 else "anthropic"
url = f"https://pypi.org/pypi/{package}/json"  # PyPI's public JSON API: no key needed
request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "bootcamp-prework"})
try:
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)
except urllib.error.HTTPError as err:
    sys.exit(f"HTTP {err.code}: the server answered with an error")
except urllib.error.URLError as err:
    sys.exit(f"Network problem: {err.reason}")
info = data["info"]
print({"name": info["name"], "latest_version": info["version"], "summary": info["summary"]})
