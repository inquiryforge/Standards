# Validation

The repository contains 24,111 hierarchy records, including 22,193 standards, substandards, indicators, and state extensions, plus 23 explicit not-applicable ELA records. The [validation result](validation-result.json) records the integrity checks.

Run the standard-library checks with:

```sh
python tools/validate.py
```

Checks cover unique IDs and paths, parent-child nesting, cycles, catalog consistency, statement and publication checksums, path lengths, relative links, subject and grade-band counts, and CTE source-cell relationships. Social studies additionally checks all 17 code scopes, all 609 standards, all 3,365 relevant source lines, and statement wording against the source layout. Grade-6 math and ELA and middle-school science have explicit reference-set checks.

The [social studies source audit](social-studies-source-audit.json) compares the 609 codes with independent PDF extraction. The [source audit](source-audit.json) checks science, arts, PE, computer science, world languages, WIDA, and health references, plus all 22,139 normative statement cells in the 52 CTE workbooks.

The source audit requires the dependencies in `requirements-validation.txt`:

```sh
python -m pip install -r requirements-validation.txt
python tools/audit_sources.py
```

GitHub Actions runs integrity checks on pushes and pull requests. Code-set and checksum checks establish coverage and consistency; they are not publisher certification of every character in every subject.
