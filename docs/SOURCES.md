# Sources and coverage boundaries

The [source manifest](../sources/manifest.json) records original URLs, edition labels, retrieval date (November 20, 2026), local filenames, and SHA-256 checksums. Sources follow the [Michigan Department of Education standards directory](https://www.michigan.gov/en/mde/Services/academic-standards) and linked state program pages. WIDA is published by the University of Wisconsin–Madison and linked by MDE.

| Publication | Edition and coverage |
| --- | --- |
| [Social studies](../sources/official/social-studies-2019.pdf) | June 2019; all 609 coded K–12 content/process expectations |
| [Mathematics](../sources/official/math.pdf) | 2010; K–8, all high-school numbered content and lettered parts, eight practices; modeling context retained |
| [English language arts](../sources/official/ela.pdf) | 2010; all grade/band tables, lettered parts, foundational skills, 32 anchors, RH/RST/WHST disciplinary literacy |
| [Science](../sources/official/science.pdf) | November 2015; 208 performance expectations plus seven Michigan extensions |
| [Arts](../sources/official/arts.pdf) | June 2011; all 960 statements across dance, music, theatre, and visual arts |
| [Computer science](../sources/official/computer-science.pdf) | May 2019; 120 content expectations, seven practices, 23 subpractices |
| [Health](../sources/official/health.pdf) | 2025 guidelines; all 406 indicators in Sections 2 and 3; Section 1 repeats selected indicators and remains a guide |
| [Physical education](../sources/official/physical-education.pdf) | 2017; 581 scoped outcomes, including the extra-period code S1.11.2. and the repeated printed S3.9.L1 in Level 2 |
| [Technology](../sources/official/technology.pdf) | 2017 MITECS; seven competencies and 28 lettered components |
| [Personal finance](../sources/official/personal-finance.pdf) | May 2023 content expectations; PF1–PF7 and printed subexpectation 4.1 |
| [World languages](../sources/official/world-languages.pdf) | 2007; eleven standards and 223 proficiency-based benchmarks |
| [English language development](../sources/official/english-language-development.pdf) | WIDA 2020; five standards and all 104 coded language expectations |
| [CTE program source inventory](../sources/cte-program-sources.json) | All 52 state-listed XLSX workbooks; individual source editions and CIP codes retained |

Page references are one-based physical PDF pages. Workbook citations identify the worksheet and original cells. Edition folders use publication versions, not retrieval years. Career Ready Practices have the explicit version label `state-workbooks`: the shared practice sheet has no independently printed adoption date. A CTE program workbook's date and a legacy matrix's own printed year can differ; both are retained.

## References and notation

Complete references identify the published standard, grade or proficiency band, and hierarchy. Math expressions use Unicode exponents or explicit `^(...)` and `_(...)` notation for raised and lowered symbols. Source footnotes remain with their records.

Source spelling and printed reference errors remain visible. [Arts code notes](../sources/arts-source-code-notes.json) document eleven repeated or inconsistent references: section-based corrections retain `source_code`, and `-occ2` is explicitly a repository disambiguator. PE's repeated S3.9.L1 is scoped to its actual Level 1 or Level 2 column. Health's `(2.3.PHW)` and `[12.2 SAF]` typography is normalized in complete repository references while printed references remain available.

Social studies uses only the official June 2019 book. The [coverage manifest](../sources/social-studies-2019-coverage.json) assigns every relevant source line to a record; [retained layout data](../sources/official/social-studies-2019-lines.json) supports offline wording checks. Repeated high-school process pages 87, 101, 119, and 135 share records; page 87 supplies primary wording, and differing occurrences are displayed as variants.

## Scope of supporting materials

Structural headings, modeling context, and repeated health content are retained without inventing additional standards. ELA explicitly marks not-applicable or later-beginning items. Health Section 3 has no K–2 indicators, as the source states. World language benchmarks follow proficiency levels, and WIDA preserves its published grade clusters and language modes.

WIDA language functions/features, proficiency descriptors, instructional examples, overview charts, and supporting appendices remain in the full source PDF; the 104 coded language expectations are the separate expectation files. Science is the performance-expectation publication linked by Michigan; external NGSS dimension elaborations are not additional Michigan expectation files.

CTE workbooks publish program competencies, aligned industry standards, indicators, and legacy matrices. Alignment duplicates within a program are consolidated with all source cells and other competency links retained. `N/A` cells and repeated spreadsheet column headers are excluded from standards. Knowledge/skill headings and shorter matrix criteria remain at their source hierarchy level. [CTE coverage](../sources/cte-coverage.json) maps every normative statement cell to its record. Heavy Equipment's state workbook publishes a condensed AED index; the full external industry manual is not reproduced by that workbook or invented here. Local district courses and unpublished materials are outside this source collection.

Publisher attribution and source terms appear in [third-party notices](../THIRD_PARTY_NOTICES.md).
