# Data format

Each record occupies one directory containing `README.md`. Child directories represent the record's standards, substandards, or organizational levels. The statement is between `<!-- standard-text:start -->` and `<!-- standard-text:end -->`. Source citations, notes, and navigation appear outside that statement.

The frontmatter uses one JSON-compatible value per YAML line. The [catalog](../catalog.json) contains the same records in JSON, with `schema_version` and `reference_date` at the top level. The [record schema](../schema/record.schema.json) describes required fields.

| Field | Meaning |
| --- | --- |
| `id` | Unique record identity, including jurisdiction, subject, edition, and scope |
| `code` | Complete standard or grouping reference |
| `source_code` | Printed reference or source position |
| `parent_id`, `children` | Explicit hierarchy relationships |
| `path` | Record file relative to the repository root |
| `subject`, `framework`, `edition` | Subject area, framework, and publication version |
| `grade_band` | Applicable grades; `0` denotes kindergarten |
| `node_type` | Standard, substandard, state extension, not-applicable item, or structural level |
| `status` | `active`, `structural`, or `not-applicable` |
| `text` | Full statement; stored in the catalog and the record's statement section |
| `text_sha256` | SHA-256 of the statement text |
| `source` | Publication identifiers, PDF pages, or workbook sheets and cells |
| `notes` | Source qualifications, footnotes, and reference details |
| `title_origin`, `code_origin` | Relationship of the title/reference to the publication |

Some records also identify proficiency, discipline, CIP program code, mathematical modeling or advanced content, source variants, or related competency alignments. Language proficiency levels and published grade clusters retain their source scope. Structural records provide navigation and context; they are not additional assessment targets.

The [source manifest](../sources/manifest.json) supplies each publication's title, authority, edition, URL, retrieval date, repository file, and checksum. PDF pages are one-based physical pages. Workbook cell references use their original worksheet coordinates.
