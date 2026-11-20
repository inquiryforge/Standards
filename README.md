# Michigan Standards

Michigan standards organized into one Markdown file per standard, with substandards nested beneath their parent. Browse by subject, source edition, grade or proficiency band, and published hierarchy. Each record links to its parent, children, and retained official source.

## Browse all subjects

| Subject | Source edition | Included coverage | Records |
| --- | --- | --- | ---: |
| [Social studies](standards/us/mi/social-studies/2019/README.md) | 2019 | K–12 content, high-school courses, and process/skills | 609 |
| [Mathematics](standards/us/mi/mathematics/2010/README.md) | 2010 | K–8, high school, advanced content, and eight mathematical practices | 517 |
| [English language arts](standards/us/mi/english-language-arts/2010/README.md) | 2010 | K–12, foundational skills, anchor standards, and disciplinary literacy | 1,022 |
| [Science](standards/us/mi/science/2015/README.md) | 2015 | K–12 performance expectations, shared engineering bands, and seven Michigan extensions | 215 |
| [Arts](standards/us/mi/arts/2011/README.md) | 2011 | Dance, music, theatre, and visual arts; K–8 and high school | 960 |
| [Computer science](standards/us/mi/computer-science/2019/README.md) | 2019 | All five levels, seven practices, and 23 subpractices | 150 |
| [Health education](standards/us/mi/health/2025/README.md) | 2025 | All indicators in Sections 2 and 3; Section 1 retained as a repeated-content guide | 406 |
| [Physical education](standards/us/mi/physical-education/2017/README.md) | 2017 | K–8 and high-school Levels 1 and 2 | 581 |
| [Technology / MITECS](standards/us/mi/technology/2017/README.md) | 2017 | Seven competencies and 28 subcompetencies | 35 |
| [Personal finance](standards/us/mi/personal-finance/2023/README.md) | 2023 | Seven high-school expectations and the printed 4.1 subexpectation | 8 |
| [World languages](standards/us/mi/world-languages/2007/README.md) | 2007 | Eleven standards and 223 proficiency-based benchmarks | 234 |
| [English language development / WIDA](standards/us/mi/english-language-development/2020/README.md) | 2020 | Five standards and all 104 coded language expectations | 109 |
| [Career and technical education](standards/us/mi/career-technical-education/README.md) | Per program | All 52 program workbooks linked by the state; competencies, standards, and indicators | 17,335 |
| [Career readiness](standards/us/mi/career-readiness/state-workbooks/README.md) | state-workbooks | Twelve shared Career Ready Practices, with workbook occurrences linked | 12 |

**22,193 standard, substandard, indicator, and state-extension records across 14 subject areas**, plus 23 explicit not-applicable ELA records and structural grouping pages. Counts include parents and their children, and career-program source headings; they are not a count of distinct assessment targets. Repeated career alignments are stored once within each program and link to their other competency parents.

The sources follow Michigan's [academic standards directory](https://www.michigan.gov/en/mde/Services/academic-standards) and its linked frameworks. All 52 state-listed CTE program workbooks are included. Some workbooks reference external industry manuals without reproducing them; this repository contains the content the state actually publishes, including its condensed index where that is all the workbook supplies.

## Social studies

All **609** unique coded K–12 content and process/skills expectations come from the official [Michigan K–12 Social Studies Standards, June 2019](sources/official/social-studies-2019.pdf). Full statements, required bullets, examples, and repeated-source variants are preserved.

## Files and codes

```text
standards/us/mi/
  social-studies/2019/grades-06-08/grade-06/
    geography/G1/G1.1/G1.1.1/README.md
  mathematics/2010/grade-06/
    6.RP/6.RP.A/6.RP.A.3/README.md
      6.RP.A.3a/README.md
```

Each folder's `README.md` is its record and GitHub landing page. `code` is the complete standard reference; `source_code` preserves the printed reference; `id` identifies its edition and scope. See [naming rules](docs/NAMING.md), [source boundaries](docs/SOURCES.md), and the searchable [catalog](catalog.json).

Browse the Markdown files or import `catalog.json` directly; neither requires Python or installed packages. The small scripts in `tools/` are for maintainers to check changes against the records and original publications. See [Validation](docs/VALIDATION.md) for the two check commands.

## Reference

- [Catalog](catalog.json): all records and their metadata.
- [Naming and hierarchy](docs/NAMING.md): codes, IDs, grades, and parent relationships.
- [Data format](docs/DATA_FORMAT.md): record fields and file structure.
- [Sources](docs/SOURCES.md): publications, editions, and coverage.
- [Validation](docs/VALIDATION.md): integrity and source checks.
- [Third-party notices](THIRD_PARTY_NOTICES.md): publisher attribution and source terms.

## License and attribution

© 2026 **InquiryForge**. Repository-original documentation, metadata, schemas, and organization are licensed under [CC BY 4.0](LICENSE). Validation software is licensed under [MIT](tools/LICENSE). Standards and source publications retain their respective publishers' rights and terms.

See [Licensing](LICENSING.md) for scope and [Attribution](ATTRIBUTION.md) for credit information.
