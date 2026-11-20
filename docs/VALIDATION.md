# Validation

The repository contains 24,111 hierarchy records, including 22,193 standards, substandards, indicators, and state extensions, plus 23 explicit not-applicable ELA records. Browsing these files or importing the catalog requires no validation tools or Python packages.

Run the standard-library checks with:

```sh
python tools/validate.py
```

Checks cover unique IDs and paths, parent-child nesting, cycles, catalog consistency, statement and publication checksums, path lengths, relative links, subject and grade-band counts, and CTE source-cell relationships. Social studies additionally checks all 17 code scopes, all 609 standards, all 3,365 relevant source lines, and statement wording against the source layout. Grade-6 math and ELA and middle-school science have explicit reference-set checks.

For a deeper source check, `audit_sources.py` independently extracts science, arts, PE, computer science, world languages, WIDA, and health references, plus all 22,139 normative statement cells in the 52 CTE workbooks.

Only this optional audit requires the dependency in [tools/requirements-audit.txt](../tools/requirements-audit.txt):

```sh
python -m pip install -r tools/requirements-audit.txt
python tools/audit_sources.py
```

Both commands print a JSON report and exit with a nonzero status if checks fail. They do not modify repository files. Generated reports are not committed: rerun the checks for the current state, or read the [GitHub Actions results](https://github.com/inquiryforge/Standards/actions/workflows/validate.yml), which run integrity checks on pushes and pull requests. If you want to save a local report, create a `reports/` directory and redirect command output there; that directory is ignored by Git.

The two helper modules support these commands: `common.py` reads the record format for validation and supplies shared constants; `cte_workbook.py` reads the source XLSX cells for the optional audit. Original PDFs, workbooks, coverage maps, and source-code notes remain in `sources/` because records cite them and checks depend on them.

The retained [social studies source audit](social-studies-source-audit.json) is the original independent PDF-extraction comparison of all 609 codes. It is historical evidence, not a report of the latest run. Current integrity checks verify those codes, source lines, and wording against the retained source layout on every run.

Code-set and checksum checks establish coverage and consistency; they are not publisher certification of every character in every subject.
