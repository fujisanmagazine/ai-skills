---
name: opensearch
description: "Analyze z86 pound access logs on Fujisan OpenSearch without data changes. Setup requires OPENSEARCH_USER and OPENSEARCH_PASSWORD in the workspace .env; see README.md."
---

# Fujisan Pound/OpenSearch Read-only Analysis

Use this skill for investigations of the Fujisan pound access logs when the user wants searches or aggregations only.

If you install this skill for a user, show the authentication setup steps in [README.md](README.md) after installation succeeds. Do not ask the user to provide the credentials in chat.

## Connection

- Read `OPENSEARCH_USER` and `OPENSEARCH_PASSWORD` from `.env` in the current workspace. Expect normal shell assignments (`KEY=value`); do not print, log, or include either value in output.
- Connect to `https://syslog.fujisan.co.jp:9200`. The cluster uses a certificate that must be accessed with certificate verification disabled (`curl --insecure`).
- Search `pound-logs-*` and scope the host with the exact term filter `fb_HOSTNAME.keyword: z86`, unless the user explicitly changes that scope.

## Safety boundary

- Treat every cluster interaction as strictly read-only. Use only `_search` and `_count` endpoints for analysis.
- Never call index-management, document-mutation, reindex, delete, update, bulk, snapshot, or settings APIs. Never create or change an index, alias, template, mapping, pipeline, task, or cluster setting.
- Do not make exploratory searches or broad aggregations unless the user asks for that specific analysis. Ask for the desired condition or metric when it is not supplied.

## Query practice

- Use a `term` query against `fb_HOSTNAME.keyword` and put other requested constraints in `bool.filter` clauses.
- For aggregations, request `size: 0`; for sample events, limit returned fields and the number of documents to the minimum needed.
- State the exact time range, timezone interpretation, filters, and any aggregation approximation (`doc_count_error_upper_bound`) in results when relevant.
- Report evidence and distinguish observations from hypotheses. If diagnosis needs a follow-up search, propose its narrowly scoped condition before running it.
