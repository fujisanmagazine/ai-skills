#!/usr/bin/env python3
"""Fetch an allowed Fujisan API documentation resource without exposing credentials."""

import base64
import os
import re
import sys
import urllib.error
import urllib.request

HOST = "https://apidoc.fujisan.co.jp"
SEGMENT = re.compile(r"[A-Za-z0-9._-]+")
USAGE = (
    "error: allowed paths are /, /api-index.json, /apis/<name> (optionally /apis/<group>/<name>), "
    "/docs/<id>, and /redocusaurus/<name>.yaml"
)


def canonical_path(path):
    """Return the path to request, or None when it is not an allowed document.

    Documentation pages are served only with a trailing slash; the bare path 301s to it.
    """
    if path in ("/", "/api-index.json"):
        return path
    if not path.startswith("/"):
        return None
    segments = path.strip("/").split("/")
    if any(segment in (".", "..") or not SEGMENT.fullmatch(segment) for segment in segments):
        return None
    if segments[0] == "redocusaurus":
        return path if len(segments) == 2 and segments[1].endswith(".yaml") else None
    if segments[0] in ("apis", "docs") and len(segments) >= 2:
        return "/" + "/".join(segments) + "/"
    return None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused", headers, fp)


def main() -> int:
    if len(sys.argv) > 2:
        print(USAGE, file=sys.stderr)
        return 2
    target = canonical_path(sys.argv[1] if len(sys.argv) == 2 else "/api-index.json")
    if target is None:
        print(USAGE, file=sys.stderr)
        return 2

    username = os.environ.get("APIDOC_BASIC_USERNAME")
    password = os.environ.get("APIDOC_BASIC_PASSWORD")
    if username is None or password is None:
        print("error: APIDOC_BASIC_USERNAME and APIDOC_BASIC_PASSWORD must be set", file=sys.stderr)
        return 2

    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        HOST + target,
        headers={"Authorization": f"Basic {token}", "Accept": "application/json, application/yaml, text/html;q=0.9"},
    )
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=20) as response:
            sys.stdout.buffer.write(response.read())
    except urllib.error.HTTPError as error:
        print(f"error: documentation request failed with HTTP {error.code}", file=sys.stderr)
        return 1
    except urllib.error.URLError:
        print("error: documentation request failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
