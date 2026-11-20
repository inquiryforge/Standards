# Naming and hierarchy

Records follow `standards/<country>/<state>/<subject>/<edition>/<grade-or-band>/<parents>/<code>/README.md`. Social studies places individual grades within their grade-band folder.

- Country/state: `us/mi`; metadata jurisdiction: `US-MI`.
- Subjects: lowercase hyphenated names, including `social-studies`, `mathematics`, `english-language-arts`, and `science`.
- Grades: `grade-06`; bands: `grades-06-08`. Social studies uses `grades-k-02`, `grades-03-05`, `grades-06-08`, and `high-school`. Each K–8 band contains its Process and Skills collection and the individual grade folders; high school contains Process and Skills and separate course folders.
- Editions: source adoption/publication edition, not download year. Social studies uses `2019`, the official June 2019 book.
- Coded folders keep full codes: `G1/G1.1/G1.1.1`. Uncoded source headings have descriptive slugs.
- Every node has one `README.md`. A parent standard keeps its statement there and contains child directories for substandards.
- Titles come from source headings when available; otherwise they are statement excerpts for navigation, marked in `title_origin`. Full wording remains in the body.

## Code and ID

| Field | Purpose | Example |
| --- | --- | --- |
| `source_code` | Printed or positional source reference | `6.RP / 3.a` |
| `code` | Familiar complete reference | `6.RP.A.3a` |
| `id` | Unique versioned repository identity | `MI.MATH.2010.6.RP.A.3a` |
| `parent_id` | Explicit parent link | `MI.MATH.2010.6.RP.A.3` |

Preserve official codes. Document source errors explicitly when a collision or printed section mismatch requires a separate repository reference. Michigan's math PDF prints domain codes and numbered expectations beneath named clusters. Cluster letters and composite references use conventional domain/cluster/standard notation and are marked `code_origin: "conventional-composite"`. ELA similarly combines strand, grade, number, and letter. These composite codes are not presented as literal PDF typography.

Civics `C – 2.1.1` has canonical code `C2.1.1`, while its printed form remains in `source_code`. A missing intermediate heading such as `W4.1` becomes an explicitly inferred structural parent, not another assessable standard.

IDs identify a specific edition and scope. Different official editions occupy separate collections. File paths, parent relationships, and catalog entries describe the same hierarchy.

## Other subject conventions

Arts uses discipline, source grade section, category, and expectation; printed errors and occurrence suffixes are documented. PE uses grade/level-scoped IDs because its source repeats one code across Level 1 and Level 2. World languages preserves proficiency codes, including the source's unusual `2.2.M.Fc`, rather than imposing grades. WIDA IDs identify the published domain, grade cluster, key language use, and mode.

CTE paths use cluster, CIP program code, workbook edition, and the source hierarchy. Native competency references such as `A1` stay intact. Uncoded aligned standards receive `S001` references and indicators receive `PI001`, marked `repository-position`; these are navigation IDs, not official industry codes. Legacy matrices use the source hierarchy's composite markers or a documented worksheet row reference. Other competency alignments link to the canonical file instead of silently duplicating its content.

Health combines the published grade-span/practice/topic reference and indicator number, marked `source-position-composite`. Source publication years, workbook versions, and explicit undated labels are distinct from the retrieval date.
