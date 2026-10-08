# Fujisan log index reference

Source: user-provided documents dated 2026-10-08. Field presence and JSON value shapes below are observed in those samples. They do not establish OpenSearch mapping types, `.keyword` availability, aggregation support, or presence in every document. Use verified mapping information when exact matching or aggregation requires it.

## Common fields

| Field | Sample value shape | Use |
|---|---|---|
| `@timestamp` | UTC ISO timestamp string | Primary search time; display in the requested timezone |
| `fb_HOSTNAME` | String | Origin server; preserve the actual hostname, including domain suffixes |
| `fluent_tag` | String | Ingestion/source classification |
| `SYSLOG_IDENTIFIER` | String | Log source identifier |
| `service.name` | String nested under `service` | Service classification |
| `fb_TRANSPORT` | String | Transport, such as `file` or `syslog` |

`_index`, `_id`, `fields`, and `sort` in the provided search responses are outside `_source`; do not treat them as source fields. Use `_index` and `_id` when identifying evidence documents.

## collect-logs-*

Aggregates logs from all servers. Select a host or service and time range appropriate to the investigation.

The sample is nginx access output from `zasshi-catalog1`, identified by `SYSLOG_IDENTIFIER: nginx/catalog-page-admin` and `fluent_tag: app.nginx.access.catalog-page-admin`.

| Field | Sample value shape | Use |
|---|---|---|
| `MESSAGE` | String | Raw log content; uppercase field name |

The sample `MESSAGE` contains tab-separated `key:value` entries: `time`, `msec`, `host`, `forwardedfor`, `req`, `method`, `uri`, `status`, `size`, `referer`, `ua`, `reqtime`, `upsttime`, `cache`, `runtime`, and `vhost`.

- These entries are embedded text, not demonstrated independently indexed fields. Do not query `status` or aggregate `reqtime` as source fields based on this sample.
- The embedded `host` value is distinct from `fb_HOSTNAME`; do not equate them. The sample's embedded `time` includes `+0900`, while `@timestamp` is UTC.
- Parse only retrieved, bounded samples when necessary. A calculation from samples is not a population-wide metric. Other services may use entirely different message formats.

## pound-logs-*

Web access logs from Pound, ELB, and API Gateway. The supplied document is Pound output from `z86`; equivalent fields for ELB and API Gateway have not been established.

| Fields | Sample value shape | Use |
|---|---|---|
| `status_code`, `response_size` | Numbers | HTTP status and response size; size unit unverified |
| `request_time` | Number | Request duration; unit unverified, do not label seconds or milliseconds until confirmed |
| `http_host`, `http_method`, `http_version` | Strings | Requested virtual host, method, and protocol |
| `uri` | String | Request URI including query string |
| `uri_path_root`, `uri_path_segment_2`, `uri_path_segment_3` | Strings | Precomputed path groupings; sample: `/cart`, `/cart/api`, `/cart/api/items` |
| `client_ip`, `client_ip_24`, `client_ip_16` | Strings | Client IP and precomputed network groups; mapping types unverified |
| `referer`, `user_agent` | Strings | Request context; may contain sensitive or attacker-controlled text |
| `upstream`, `proxy_from` | Strings | Proxy/upstream context; sample `proxy_from` is `-` |
| `country_code`, `country_name`, `asn_org` | Strings | Enriched client classification |
| `asn` | Number | Enriched ASN |
| `status_code_str` | String | String representation of status |
| `access_time` | String | Original access timestamp with timezone offset |
| `fb__REALTIME_TIMESTAMP` | String | Original transport timestamp; use `@timestamp` for common time filtering |
| `user_agent_info` | Object | Parsed browser, OS, and device information |

- For endpoint rankings, choose full URI or path grouping based on the question. Full URI can split one endpoint across many query parameter values. Do not describe a path-prefix bucket as an exact endpoint.
- When analyzing multiple source types, account for missing fields and explain metric coverage. Do not apply the Pound schema to ELB/API Gateway without evidence.

## windows-event-logs-*

Windows events structured for analysis. The sample is a Security event from `DB5.fujisan.local`, with `EventID: 4624` and `EventType: AUDIT_SUCCESS`.

| Fields | Sample value shape | Use |
|---|---|---|
| `EventID` | Number | Event identifier |
| `Channel`, `SourceName`, `Category` | Strings | Event channel, provider, and category |
| `EventType`, `Severity`, `LOG_LEVEL` | Strings | Event classifications; do not assume all express the same dimension |
| `SeverityValue`, `OpcodeValue` | Numbers | Source-provided numeric classifications |
| `Message` | String | Rendered event text; mixed-case name, distinct from collect's `MESSAGE` |
| `TargetUserName`, `TargetDomainName`, `TargetUserSid` | Strings | Target account context |
| `SubjectUserName`, `SubjectDomainName`, `SubjectUserSid` | Strings | Subject account context; distinct from target |
| `LogonType` | String | Sample is `"8"`; do not assume a numeric mapping |
| `IpAddress`, `IpPort`, `WorkstationName` | Strings | Network context; sample IP and port are `-` |
| `ProcessName`, `AuthenticationPackageName`, `LogonProcessName` | Strings | Process and authentication context |
| `TargetLogonId`, `SubjectLogonId`, `LogonGuid`, `ActivityID` | Strings | Possible correlation identifiers; semantics depend on event/source |
| `Hostname` | String | Additional hostname field; common host filtering uses `fb_HOSTNAME` |
| `RecordNumber`, `ProcessID`, `ThreadID`, `Version` | Numbers | Source event metadata |
| `EventTime`, `EventReceivedTime` | Strings without offset | Original event and receipt timestamps; timezone unverified |

- Exclude or separately report `-`, empty, and missing values in network/account metrics; they are not real addresses or account identities.
- Do not substitute receipt time for event time or assign a timezone to offset-free timestamps without confirmation.
- Windows events may also be present in `collect-logs-*`; overlap and deduplication keys are unverified. Report counts per index unless independence or a valid deduplication method is established.
