---
name: fujisan-api-docs
description: Consult the Fujisan API's authoritative documentation for specifications and examples; never call business APIs. Setup requires APIDOC_BASIC_USERNAME and APIDOC_BASIC_PASSWORD; see README.md.
---

# Fujisan API documentation

Use `https://apidoc.fujisan.co.jp/` as the primary and authoritative source for Fujisan API specifications. This skill is strictly for reading API documentation and preparing code examples. Do not call an operational, business, or write API.

If you install this skill for a user, show the authentication setup steps in [README.md](README.md) after installation succeeds. Do not ask the user to provide the credentials in chat.

## Credentials and safety

- Use `APIDOC_BASIC_USERNAME` and `APIDOC_BASIC_PASSWORD` only at execution time. Do not ask users to paste them into chat.
- Never put either value in Git, `SKILL.md`, `.codex/config.toml`, generated code, logs, command arguments, or command output.
- Use `scripts/fetch_apidoc.py` for every documentation fetch. It fixes the host and accepts only approved documentation paths; do not use `curl`, a browser URL field, or a general HTTP client for this site.
- The script prints only the retrieved document. Redirect output to a temporary file when inspection requires more than a short response, and remove the file after use.

## Documentation discovery

1. Fetch `/api-index.json` first:

   ```sh
   python3 scripts/fetch_apidoc.py /api-index.json
   ```

   Every entry has `name`, `title`, `version`, `documentation_url`, and `openapi_url`. The values are site-relative paths, so pass them to the fetch script unchanged.

2. The catalog lists REST APIs only. GraphQL APIs appear as `/docs/<id>` links on `/`, so fetch `/` as well whenever the question is not answered by a catalog entry.

3. For a REST API, fetch `openapi_url` and consult its OpenAPI YAML for exact operations, schemas, examples, and the `servers` URLs for Alpha, Beta, and Live. Consult `documentation_url` for the human-readable reference. For a GraphQL API, consult its `/docs/<id>` page.

4. Base any answer on the retrieved primary documentation. State uncertainty rather than inventing endpoints, parameters, authentication methods, or response shapes.

## Producing an answer or example

- Identify the API and operation, HTTP method, path, required parameters, authentication scheme, request body, and notable error responses from the documentation.
- Before writing a REST API sample app or request code, read the fetched OpenAPI YAML's `servers` section and use its URL for the intended Alpha, Beta, or Live environment as the API base URL. Combine that base URL with the documented operation path. Do not substitute `localhost`, `127.0.0.1`, or an invented host for a server URL. If the environment is unspecified, make the choice explicit in the sample or ask which one to use; if the YAML does not establish the URL, ask rather than guessing.
- Make examples use placeholders such as `YOUR_API_KEY` and `YOUR_VALUE`; never include real credentials or make a network request to a Fujisan business API.
- Clearly label assumptions when the docs do not establish a detail.
- Cite the relevant documentation and OpenAPI URL in the response when useful.

## Script location

The bundled script is at `scripts/fetch_apidoc.py`, relative to this skill directory. Run the commands above from the skill directory. For a local credentials file, use `scripts/with-apidoc-creds.sh` to load it before running the fetch script.
