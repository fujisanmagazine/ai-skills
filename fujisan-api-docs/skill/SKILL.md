---
name: fujisan-api-docs
description: Consult the Fujisan API's authoritative documentation to answer specification, endpoint, and request-example questions. Use only for API documentation and code examples; never call Fujisan business APIs.
---

# Fujisan API documentation

Use `https://apidoc.fujisan.co.jp/` as the primary and authoritative source for Fujisan API specifications. This skill is strictly for reading API documentation and preparing code examples. Do not call an operational, business, or write API.

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

3. For a REST API, consult `documentation_url` for the human-readable reference and `openapi_url` for exact operations, schemas, and examples. For a GraphQL API, consult its `/docs/<id>` page.

4. Base any answer on the retrieved primary documentation. State uncertainty rather than inventing endpoints, parameters, authentication methods, or response shapes.

## Producing an answer or example

- Identify the API and operation, HTTP method, path, required parameters, authentication scheme, request body, and notable error responses from the documentation.
- Make examples use placeholders such as `YOUR_API_KEY` and `YOUR_VALUE`; never include real credentials or make a network request to a Fujisan business API.
- Clearly label assumptions when the docs do not establish a detail.
- Cite the relevant documentation and OpenAPI URL in the response when useful.

## Script location

The bundled script is at `scripts/fetch_apidoc.py`, relative to this skill directory. The commands above use that relative path, so run them from the skill directory. When working from this repository rather than an installed skill, the path is `skill/scripts/fetch_apidoc.py`.
